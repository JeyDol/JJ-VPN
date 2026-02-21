from decimal import Decimal
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.vpn.core.exceptions import InvalidAmountException, NotFoundException, InsufficientBalanceException
from src.vpn.db.models.users import UsersOrm
from src.vpn.repositories.base import BaseRepository
from src.vpn.repositories.mappers.base import DataMapper
from src.vpn.repositories.mappers.mappers import UsersDataMapper
from src.vpn.schemas.users import UserRead


class UsersRepository(BaseRepository):
    model = UsersOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session, UsersDataMapper)


    async def get_by_telegram_id(self, tg_id: int) -> UserRead | None:
        stmt = select(self.model).where(self.model.telegram_id == tg_id)
        result = await self.session.execute(stmt)
        data = result.scalar_one_or_none()
        if data is None:
            return None
        return self.mapper.map_to_domain_entity(data)

    async def add_balance(self, user_id: int, amount: Decimal) -> UserRead:
        if amount <= 0:
            raise InvalidAmountException(float(amount), "Сумма должна быть положительным")

        stmt = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()

        if db_obj is None:
            raise NotFoundException("User", user_id)
        db_obj.balance +=amount

        await self.session.commit()
        await self.session.refresh(db_obj)
        return self.mapper.map_to_domain_entity(db_obj)


    async def deduct_balance(self, user_id: int, amount: Decimal):
        if amount <= 0:
            raise InvalidAmountException(float(amount), "Сумма должна быть положительной")

        stmt = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()

        if db_obj is None:
            raise NotFoundException("User", user_id)

        if db_obj.balance < amount:
            raise InsufficientBalanceException(user_id, required=float(amount), available=float(db_obj.balance))
        db_obj.balance -= amount

        await self.session.commit()
        await self.session.refresh(db_obj)
        return self.mapper.map_to_domain_entity(db_obj)

    #к этому методу селери таску сделать
    async def get_users_with_low_balance(self, threshold: Decimal = Decimal("30.00")) -> List[UserRead]:
        stmt = select(self.model).where(self.model.balance <= threshold, self.model.is_active == True)
        result = await self.session.execute(stmt)
        db_objs = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in db_objs]


    async def deactivate(self, user_id: int) -> UserRead:
        stmt = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            raise NotFoundException("User", user_id)
        db_obj.is_active = False
        await self.session.commit()
        await self.session.refresh(db_obj)
        return self.mapper.map_to_domain_entity(db_obj)


    async def activate(self, user_id: int) -> UserRead:
        stmt = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            raise NotFoundException("User", user_id)
        db_obj.is_active = True
        await self.session.commit()
        await self.session.refresh(db_obj)
        return self.mapper.map_to_domain_entity(db_obj)


