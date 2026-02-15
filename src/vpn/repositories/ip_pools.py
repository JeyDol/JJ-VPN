from datetime import datetime

from sqlalchemy import select

from src.vpn.core.exceptions import NotFoundException, NoAvailableIPException
from src.vpn.db.models.ip_pools import IPPoolsOrm
from src.vpn.repositories.base import BaseRepository
from src.vpn.repositories.mappers.base import DataMapper
from src.vpn.repositories.mappers.mappers import IPPoolsDataMapper
from src.vpn.schemas.ip_pools import IPPoolRead


class IPPoolRepository(BaseRepository):
    model = IPPoolsOrm
    mapper: DataMapper = IPPoolsDataMapper


    async def get_first_free(self) -> IPPoolRead:
        stmt = select(self.model).where(self.model.is_allocated == False).limit(1)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            raise NoAvailableIPException()
        return self.mapper.map_to_domain_entity(db_obj)


    async def allocate_to_peer(self, ip_id: int, peer_id: int) -> IPPoolRead:
        stmt = select(self.model).where(self.model.id == ip_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            raise NotFoundException("IPPool", ip_id)
        db_obj.is_allocated = True
        db_obj.peer_id = peer_id
        db_obj.allocated_at = datetime.now()

        await self.session.commit()
        await self.session.refresh(db_obj)
        return self.mapper.map_to_domain_entity(db_obj)


    async def release_by_id(self, ip_id: int) -> IPPoolRead:
        stmt = select(self.model).where(self.model.id == ip_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            raise NotFoundException("IPPool", ip_id)
        db_obj.is_allocated = False
        db_obj.peer_id = None
        db_obj.allocated_at =db_obj.allocated_at

        await self.session.commit()
        await self.session.refresh(db_obj)
        return self.mapper.map_to_domain_entity(db_obj)

