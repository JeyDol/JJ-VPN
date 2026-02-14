from typing import TypeVar, Type
from pydantic import BaseModel
from src.vpn.db.base import Base  # твой SQLAlchemy Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class DataMapper:
    db_model: Type[DBModelType] = None
    schema: Type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, db_obj: DBModelType) -> SchemaType:
        """
        Преобразует объект БД в Pydantic-схему
        """
        return cls.schema.model_validate(db_obj, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, schema_obj: SchemaType) -> DBModelType:
        data = schema_obj.model_dump(exclude_unset=True, exclude_none=True)
        return cls.db_model(**data)
