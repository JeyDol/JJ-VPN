from src.vpn.db.models.peers import PeersOrm
from src.vpn.repositories.base import BaseRepository
from src.vpn.repositories.mappers.base import DataMapper
from src.vpn.repositories.mappers.mappers import PeersDataMapper


class PeersRepository(BaseRepository):
    model = PeersOrm
    mapper: DataMapper = PeersDataMapper

    