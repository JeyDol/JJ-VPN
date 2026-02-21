from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.vpn.core.exceptions import NotFoundException, InvalidAmountException
from src.vpn.db.dependencies import get_user_service, get_transaction_repository
from src.vpn.repositories.transactions import TransactionsRepository
from src.vpn.schemas.transactions import TransactionRead
from src.vpn.schemas.users import UserRead
from src.vpn.services.users import UsersService

router = APIRouter(prefix="/users", tags=["Users"])


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
