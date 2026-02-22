from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.vpn.core.exceptions import ValidationException, NotFoundException
from src.vpn.db.dependencies import get_peers_service, get_peer_repository, get_current_user
from src.vpn.repositories.peers import PeersRepository
from src.vpn.schemas.peers import PeerRead
from src.vpn.schemas.users import UserRead
from src.vpn.services.peers import PeersService

router = APIRouter(prefix="/peers", tags=["Peers"])


admin_router = APIRouter(prefix="/admin/peers", tags=["Admin - Peers"])

@router.post("/", response_model=PeerRead, status_code=201)
async def create_peer(
        device_name: str = "Устройство",
        current_user: UserRead = Depends(get_current_user),
        peer_service: PeersService = Depends(get_peers_service)
):
    try:
        peer = await peer_service.create_peer(user_id=current_user.id, device_name=device_name)
        return peer
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get("/", response_model=List[PeerRead])
async def get_my_peers(
        current_user: UserRead = Depends(get_current_user),
        peer_service: PeersService = Depends(get_peers_service)
):
    peers = await peer_service.get_user_peers(current_user.id)
    return peers


@router.get("/{peer_id}/config", response_model=dict)
async def get_peer_config(
        peer_id: int,
        current_user: UserRead = Depends(get_current_user),
        peer_service: PeersService = Depends(get_peers_service)
):
    try:
        peer = await peer_service.peer_repo.get_by_id(peer_id)

        if peer is None:
            raise HTTPException(status_code=404, detail="Peer не найден")

        if peer.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="У вас нет доступа к этому peer'у"
            )

        # Генерируем конфиг
        config = await peer_service.get_peer_config(
            peer_id,
            server_address="",
            server_port=2053
        )

        return {
            "vless_link": config.to_vless_link(),
            "device_name": config.device_name,
            "uuid": config.uuid
        }
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post("/{peer_id}/deactivate", response_model=PeerRead)
async def deactivate_peer(
        peer_id: int,
        current_user: UserRead = Depends(get_current_user),
        peer_service: PeersService = Depends(get_peers_service)
):
    try:
        peer = await peer_service.peer_repo.get_by_id(peer_id)

        if peer is None:
            raise HTTPException(status_code=404, detail="Peer не найден")

        if peer.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="У вас нет доступа к этому peer'у"
            )

        peer = await peer_service.deactivate_peer(peer_id)
        return peer
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/{peer_id}", status_code=204)
async def delete_peer(
        peer_id: int,
        current_user: UserRead = Depends(get_current_user),
        peer_service: PeersService = Depends(get_peers_service)
):
    try:
        await peer_service.delete_peer(peer_id, current_user.id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ValidationException as e:
        raise HTTPException(status_code=403, detail=e.detail)


@admin_router.get("", response_model=List[PeerRead])
async def get_all_peers(
        peer_repo: PeersRepository = Depends(get_peer_repository)
):
    peers = await peer_repo.get_all()
    return peers


@admin_router.get("/active", response_model=List[PeerRead])
async def get_all_active_peers(
        peer_repo: PeersRepository = Depends(get_peer_repository)
):
    peers = await peer_repo.get_all_active()
    return peers


@admin_router.delete("/{peer_id}", status_code=204)
async def force_delete_peer(
        peer_id: int,
        peer_repo: PeersRepository = Depends(get_peer_repository)
):
    deleted = await peer_repo.delete(peer_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Peer не найден")
