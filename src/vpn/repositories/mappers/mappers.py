from src.vpn.db.models.ip_pools import IPPoolsOrm
from src.vpn.db.models.peers import PeersOrm
from src.vpn.db.models.users import UsersOrm
from src.vpn.repositories.mappers.base import DataMapper
from src.vpn.schemas.ip_pools import IPPoolRead, IPPoolCreate
from src.vpn.schemas.peers import PeerRead, PeerCreate, PeerUpdate
from src.vpn.schemas.users import UserRead, UserCreate, UserUpdate


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


class PeersDataMapper(DataMapper):
    db_model = PeersOrm
    schema = PeerRead

    @classmethod
    def from_create(cls, schema_obj: PeerCreate) -> PeersOrm:
        data = schema_obj.model_dump(exclude_unset=True, exclude_none=True)
        return cls.db_model(**data)

    @classmethod
    def apply_update(cls, db_obj: PeersOrm, schema_obj: PeerUpdate) -> PeersOrm:
        data = schema_obj.model_dump(exclude_unset=True, exclude_none=True)
        for k, v in data.items():
            setattr(db_obj, k, v)
        return db_obj


class IPPoolsDataMapper(DataMapper):
    db_model = IPPoolsOrm
    schema = IPPoolRead

    @classmethod
    def from_create(cls, schema_obj: IPPoolCreate) -> IPPoolsOrm:
        data = schema_obj.model_dump(exclude_unset=True, exclude_none=True)
        return cls.db_model(**data)