from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.vpn.core.security import verify_token
from src.vpn.db.base import get_session
from src.vpn.repositories.peers import PeersRepository
from src.vpn.repositories.transactions import TransactionsRepository
from src.vpn.repositories.users import UsersRepository
from src.vpn.schemas.users import UserRead
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

security = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        user_repo: UsersRepository = Depends(get_user_repository)
) -> UserRead:

    token = credentials.credentials

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Токен невалидный или истёк",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Извлекаем user_id
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Некорректный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: UserRead = await user_repo.get_by_id(user_id)  # type: ignore

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Пользователь не найден"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="Аккаунт деактивирован"
        )

    return user