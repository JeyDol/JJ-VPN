from src.vpn.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    schema: DataMapper = None

    def __init__(self, session, mapper: DataMapper):
        self.session = session
        self.mapper = mapper

