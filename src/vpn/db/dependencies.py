from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.vpn.db.base import AsyncSessionLocal, get_session
from src.vpn.repositories.ip_pools import IPPoolRepository
from src.vpn.repositories.peers import PeersRepository
from src.vpn.repositories.transactions import TransactionsRepository
from src.vpn.repositories.users import UsersRepository


async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UsersRepository:
    return UsersRepository(session)


async def get_peer_repository(session: AsyncSession = Depends(get_session)) ->PeersRepository:
    return PeersRepository(session)


async def get_ip_pool_repository(session: AsyncSession = Depends(get_session)) -> IPPoolRepository:
    return IPPoolRepository(session)


async def get_transaction_repository(session: AsyncSession = Depends(get_session)) -> TransactionsRepository:
    return TransactionsRepository(session)