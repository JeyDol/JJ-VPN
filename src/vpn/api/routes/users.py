from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.vpn.core.exceptions import NotFoundException, InvalidAmountException
from src.vpn.core.security import create_access_token
from src.vpn.db.dependencies import get_user_service, get_transaction_repository, get_user_repository
from src.vpn.repositories.transactions import TransactionsRepository
from src.vpn.repositories.users import UsersRepository
from src.vpn.schemas.transactions import TransactionRead
from src.vpn.schemas.users import UserRead
from src.vpn.services.users import UsersService

router = APIRouter(prefix="/users", tags=["Users"])


admin_router = APIRouter(prefix="/admin", tags=["Admin - Users"])

@router.post("/auth", response_model=UserRead)
async def auth_user(
        telegram_id: int,
        user_service: UsersService = Depends(get_user_service)
):
    user = await user_service.get_or_create_user(telegram_id)
    return user


@router.get("/me", response_model=UserRead)
async def get_my_profile(
        user_id: int,
        user_service: UsersService = Depends(get_user_service)
):
    try:
        user: UserRead = await user_service.user_repo.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        return user
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post("/balance/add", response_model=UserRead)
async def add_balance(
        user_id: int,
        amount: Decimal,
        payment_provider: str = "manual",
        user_service: UsersService = Depends(get_user_service)
):
    try:
        user = await user_service.add_balance_with_transaction(user_id=user_id, amount=amount, payment_provider=payment_provider)
        return user
    except InvalidAmountException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get("/balance/history", response_model=List[TransactionRead])
async def get_balance_history(
        user_id: int,
        trans_repo: TransactionsRepository = Depends(get_transaction_repository)
):
    try:
        history = await trans_repo.get_all_by_user_id(user_id)
        return history
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get("/can-create-peer", response_model=dict)
async def can_create_peer(
        user_id: int,
        user_service: UsersService = Depends(get_user_service)
):
    user = await user_service.can_create_peer(user_id)
    return user


@router.post("/auth/token")
async def get_auth_token(
        telegram_id: int,
        user_service: UsersService = Depends(get_user_service)
):
    user = await user_service.get_or_create_user(telegram_id)

    access_token = create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@admin_router.get("/", response_model=List[UserRead])
async def get_all_users(
        user_repo: UsersRepository = Depends(get_user_repository)
):
    users = await user_repo.get_all()
    return users


@admin_router.post("/{user_id}/ban", response_model=UserRead)
async def ban_user(
        user_id: int,
        user_repo: UsersRepository = Depends(get_user_repository)
):
    try:
        user = await user_repo.deactivate(user_id)
        return user
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@admin_router.post("/{user_id}/unban", response_model=UserRead)
async def unban_user(
        user_id: int,
        user_repo: UsersRepository = Depends(get_user_repository)
):
    try:
        user = await user_repo.activate(user_id)
        return user
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@admin_router.post("/{user_id}/balance/set", response_model=UserRead)
async def set_user_balance(
        user_id: int,
        new_balance: Decimal,
        user_repo: UsersRepository = Depends(get_user_repository)
):
    try:
        user = await user_repo.update(user_id,{"balance": new_balance}) #type: ignore
        return user
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@admin_router.get("/low-balance", response_model=List[UserRead])
async def get_users_with_low_balance(
        threshold: Decimal = Decimal("20.00"),
        user_repo: UsersRepository = Depends(get_user_repository)
):
    users = await user_repo.get_users_with_low_balance(threshold)
    return users


