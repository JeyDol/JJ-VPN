from datetime import datetime, date, timedelta
from typing import List

from sqlalchemy import select, func, or_

from src.vpn.core.exceptions import NotFoundException
from src.vpn.db.models.peers import PeersOrm
from src.vpn.repositories.base import BaseRepository
from src.vpn.repositories.ip_pools import IPPoolRepository
from src.vpn.repositories.mappers.base import DataMapper
from src.vpn.repositories.mappers.mappers import PeersDataMapper
from src.vpn.schemas.peers import PeerRead


class PeersRepository(BaseRepository):
    model = PeersOrm
    mapper: DataMapper = PeersDataMapper


    async def get_all_by_user_id(self, user_id: int) -> List[PeerRead]:
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        db_objs = result.scalars().all()
        return[self.mapper.map_to_domain_entity(obj)for obj in db_objs]


    async def get_active_by_user_id(self, user_id: int) -> List[PeerRead]:
        stmt = select(self.model).where(self.model.user_id == user_id, self.model.is_active == True)
        result = await self.session.execute(stmt)
        db_obj = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in db_obj]


    async def get_all_active(self) -> List[PeerRead]:
        stmt = select(self.model).where(self.model.is_active == True)
        result = await self.session.execute(stmt)
        db_obj = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in db_obj]


    async def deactivate_by_id(self, peer_id: int) -> PeerRead:
        stmt = select(self.model).where(self.model.id == peer_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            raise NotFoundException("Peer", peer_id)
        db_obj.is_active = False
        db_obj.revoked_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(db_obj)
        return self.mapper.map_to_domain_entity(db_obj)


    async def reactivate_by_id(self, peer_id: int) -> PeerRead:
        stmt = select(self.model).where(self.model.id == peer_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            raise NotFoundException("Peer", peer_id)
        db_obj.is_active = True
        db_obj.revoked_at = None
        await self.session.commit()
        await self.session.refresh(db_obj)
        return self.mapper.map_to_domain_entity(db_obj)


    async def count_active_by_user_id(self, user_id: int) -> int:
        stmt = select(func.count(self.model.id)).where(self.model.user_id == user_id, self.model.is_active == True)
        result = await self.session.execute(stmt)
        count = result.scalar()
        return count


    async def get_all_ready_for_billing(self) -> List[PeerRead]:
        today = date.today()
        stmt = select(self.model).where(self.model.is_active == True, or_(self.model.last_charge_date != today, self.model.last_charge_date.is_(None)))
        result = await self.session.execute(stmt)
        db_objs = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in db_objs]

    async def delete_old_inactive(self, days: int = 30) -> int:
        cutoff_date = datetime.now() - timedelta(days=days)

        stmt = select(self.model).where(self.model.is_active == False, self.model.revoked_at < cutoff_date)

        result = await self.session.execute(stmt)
        old_peers = result.scalars().all()

        for peer in old_peers:
            await self.session.delete(peer)

        await self.session.commit()
        return len(old_peers)
