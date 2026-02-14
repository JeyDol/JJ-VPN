from src.vpn.db.models.users import UsersOrm
from src.vpn.repositories.mappers.base import DataMapper


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserRead

    @classmethod
    def from_create(cls, schema_obj: UserCreate) -> UsersOrm:
        data = schema_obj.model_dump(exclude_unset=True, exclude_none=True)
        return cls.db_model(**data)

    @classmethod
    def apply_update(cls, db_obj: UsersOrm, schema_obj: UserUpdate) -> UsersOrm:
        data = schema_obj.model_dump(exclude_unset=True, exclude_none=False)
        for k, v in data.items():
            setattr(db_obj, k, v)
        return db_obj