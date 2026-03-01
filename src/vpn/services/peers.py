from typing import List
import subprocess
from pathlib import Path

from src.vpn.core.config import settings
from src.vpn.core.exceptions import ValidationException, NotFoundException
from src.vpn.repositories.peers import PeersRepository
from src.vpn.schemas.peers import PeerRead, PeerCreate, VLESSConfig
from src.vpn.services.users import UsersService
import uuid as uuid_lib


class PeersService:
    def __init__(self, peer_repo: PeersRepository, user_serv: UsersService):
        self.peer_repo = peer_repo
        self.user_serv  = user_serv


    async def create_peer(self, user_id: int , device_name: str = "Устройство") -> PeerRead:
        check = await self.user_serv.can_create_peer(user_id)

        if not check["can_create"]:
            raise ValidationException("peer_creation", check["reason"])

        client_uuid = str(uuid_lib.uuid4())

        peer = await self.peer_repo.add( # type: ignore
            PeerCreate(                            # type: ignore
                user_id=user_id,
                uuid=client_uuid,                   # type: ignore
                device_name=device_name             # type: ignore
            )
        )  # type: ignore

        try:
            self._add_user_to_xray(client_uuid, f"user-{user_id}")
        except Exception as e:
            await self.peer_repo.delete(peer.id)
            raise ValidationException(
                "xray_error",
                f"Ошибка добавления в Xray: {str(e)}"
            )

        return peer #type: ignore


    def _add_user_to_xray(self, uuid: str, email: str):
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "manage_xray.py"

        result = subprocess.run(
            ["python3", str(script_path), "add", uuid, email],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"Ошибка Xray: {result.stderr}")

    async def get_peer_config(self, peer_id: int) -> VLESSConfig:
        peer = await self.peer_repo.get_by_id(peer_id)

        if peer is None:
            raise NotFoundException("Peer", peer_id)

        config = VLESSConfig(
            peer_id=peer.id,
            uuid=peer.uuid,
            device_name=peer.device_name,
            server_address=settings.XRAY_SERVER_ADDRESS,
            server_port=settings.XRAY_SERVER_PORT,
            public_key=settings.XRAY_PUBLIC_KEY,
            short_id=settings.XRAY_SHORT_ID,
            sni=settings.XRAY_SNI,
            fingerprint=settings.XRAY_FINGERPRINT
        )

        return config


    async def get_user_peers(self, user_id: int) -> List[PeerRead]:
        peers = await self.peer_repo.get_all_by_user_id(user_id)
        return peers


    async def deactivate_peer(self, peer_id: int) -> PeerRead:
        peer = await self.peer_repo.deactivate_by_id(peer_id)
        return peer


    async def delete_peer(self, peer_id: int, user_id: int) -> bool:
        peer = await self.peer_repo.get_by_id(peer_id)

        if peer is None:
            raise NotFoundException("Peer", peer_id)

        if peer.user_id != user_id:
            raise ValidationException(
                "peer_deletion",
                f"Peer {peer_id} не принадлежит пользователю {user_id}"
            )

        try:
            self._remove_user_from_xray(peer.uuid)
        except Exception as e:
            print(f"Предупреждение: не удалось удалить из Xray: {e}")

        deleted = await self.peer_repo.delete(peer_id)
        return deleted


    def _remove_user_from_xray(self, uuid: str):
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "manage_xray.py"

        result = subprocess.run(
            ["python3", str(script_path), "remove", uuid],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"Ошибка Xray: {result.stderr}")


