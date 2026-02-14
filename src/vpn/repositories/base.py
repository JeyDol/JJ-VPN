from typing import List

from sqlalchemy import select
from sqlalchemy.sql.sqltypes import SchemaType

from src.vpn.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    schema: DataMapper = None

    def __init__(self, session, mapper: DataMapper):
        self.session = session
        self.mapper = mapper


    async def get_by_id(self, obj_id: int) -> SchemaType | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            return None
        return self.mapper.map_to_domain_entity(db_obj)


    async def get_all(self) -> List[SchemaType]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        db_objs = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in db_objs]


    async def add(self, schema_obj: SchemaType) -> SchemaType:
        db_obj = self.mapper.map_to_persistence_entity(schema_obj)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        result = self.mapper.map_to_domain_entity(db_obj)
        return result


    async def update(self, schema_obj: SchemaType, obj_id: int) -> SchemaType:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            return None
        updated_data = schema_obj.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in updated_data.items():
            setattr(db_obj, field, value)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return self.mapper.map_to_domain_entity(db_obj)


    async def delete(self, obj_id: int) -> bool:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            return False
        await self.session.delete(db_obj)
        await self.session.commit()
        return True



