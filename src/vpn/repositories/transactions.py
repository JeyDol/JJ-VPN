from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.vpn.db.models.transactions import TransactionsOrm, TransactionType
from src.vpn.repositories.base import BaseRepository
from src.vpn.repositories.mappers.base import DataMapper
from src.vpn.repositories.mappers.mappers import TransactionsDataMapper
from src.vpn.schemas.transactions import TransactionRead


class TransactionsRepository(BaseRepository):
    model = TransactionsOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session, TransactionsDataMapper)


    async def get_all_by_user_id(self, user_id: int) -> List[TransactionRead]:
        stmt = select(self.model).where(self.model.user_id == user_id).order_by(self.model.created_at.desc())
        result = await self.session.execute(stmt)
        db_obj = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in db_obj]


    async def get_deposits_by_user_id(self, user_id: int) -> List[TransactionRead]:
        stmt = select(self.model).where( self.model.user_id == user_id,self.model.type == TransactionType.DEPOSIT).order_by(self.model.created_at.desc())
        result = await self.session.execute(stmt)
        db_objs = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in db_objs]


    async def get_charges_by_user_id(self, user_id: int) -> List[TransactionRead]:
        stmt = select(self.model).where(self.model.user_id == user_id, self.model.type == TransactionType.CHARGE).order_by(self.model.created_at.desc())
        result = await self.session.execute(stmt)
        db_objs = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in db_objs]


    async def get_all_by_peer_id(self, peer_id: int) -> List[TransactionRead]:
        stmt = select(self.model).where(self.model.peer_id == peer_id).order_by(self.model.created_at.desc())
        result = await self.session.execute(stmt)
        db_objs = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in db_objs]