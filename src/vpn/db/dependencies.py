from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.vpn.db.base import get_session
from src.vpn.repositories.peers import PeersRepository
from src.vpn.repositories.transactions import TransactionsRepository
from src.vpn.repositories.users import UsersRepository
from src.vpn.services.peers import PeersService
from src.vpn.services.users import UsersService


async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UsersRepository:
    return UsersRepository(session)


async def get_peer_repository(session: AsyncSession = Depends(get_session)) ->PeersRepository:
    return PeersRepository(session)


async def get_transaction_repository(session: AsyncSession = Depends(get_session)) -> TransactionsRepository:
    return TransactionsRepository(session)


async def get_user_service(
        user_repo: UsersRepository = Depends(get_user_repository),
        peer_repo: PeersRepository = Depends(get_peer_repository),
        transaction_repo: TransactionsRepository = Depends(get_transaction_repository)
)-> UsersService:
    return UsersService(
        user_repo=user_repo,
        peer_repo=peer_repo,
        trans_repo=transaction_repo
    )


async def get_peers_service(
    peer_repo: PeersRepository = Depends(get_peer_repository),
    user_service: UsersService = Depends(get_user_service)
) -> PeersService:
    return PeersService(
        peer_repo=peer_repo,
        user_serv=user_service
    )