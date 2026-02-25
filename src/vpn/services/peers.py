from typing import List

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

        return peer     # type: ignore


    async def get_peer_config(self, peer_id: int, server_address: str = "", server_port: int = 443, use_fallback: bool = False) -> VLESSConfig:
        if use_fallback:
            server_port = 2053

        peer = await self.peer_repo.get_by_id(peer_id)

        if peer is None:
            raise NotFoundException("Peer", peer_id)

        config = VLESSConfig(
            peer_id=peer.id,
            uuid=peer.uuid,
            device_name=peer.device_name,
            server_address=server_address,
            server_port=server_port,
            public_key="aFnq58nHO19XwuMym6rTMxSU_k-8NBTBeP0PbPuKTlI",
            short_id="5dab711cddd2dbca",
            sni="www.google.com"
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

        deleted = await self.peer_repo.delete(peer_id)
        return deleted

