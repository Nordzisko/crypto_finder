import importlib

from sqlalchemy.schema import MetaData
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from crypto_finder.config import db_option
from crypto_finder.models.base import BaseModelMixin
from crypto_finder.utils import get_package_contents


class DatabaseManager:
    """
    Configuration class for DB that encapsulates engine and configured class for creating scoped session instances.
    """

    def __init__(self):
        ###
        # Private database engine and metadata attributes.
        #
        self._engine = None
        self._metadata = MetaData(schema=db_option("schema"))

        ###
        # Declarative Base Model class.
        #
        self.BaseModel = declarative_base(
            cls=BaseModelMixin, metadata=MetaData(schema=db_option("schema"))
        )

    @property
    def engine(self) -> Engine:
        return self._engine

    @classmethod
    def create_database_engine(cls) -> Engine:
        """
        Creates a new SQLAlchemy database engine (sqlalchemy.engine.base.Engine) and returns it.

        :return: a working SQLAlchemy database engine
        """
        cfg_host = db_option("host")
        cfg_port = db_option("port")
        cfg_dbname = db_option("database")
        cfg_user = db_option("user")

        # Database connection pool settings
        min_pool_size = int(db_option("min_connection_pool_size"))
        max_pool_size = int(db_option("max_connection_pool_size"))

        if max_pool_size < min_pool_size:
            raise ValueError("Max Pool Size cannot be lower than Min Pool Size!")

        max_pool_overflow = max_pool_size - min_pool_size
        pool_recycle_time = int(db_option("connection_pool_recycle_time"))

        # Database connection string
        db_uri = f"postgresql+asyncpg://{cfg_user}@{cfg_host}:{cfg_port}/{cfg_dbname}"

        return create_async_engine(
            db_uri,
            encoding="utf-8",
            pool_size=min_pool_size,
            max_overflow=max_pool_overflow,
            pool_recycle=pool_recycle_time,
            echo=True,
        )

    def init_db_engine(self):
        """
        Initialize DB engine and prepare factory session class
        """
        self._engine = self.create_database_engine()
        # Create the session factory class
        self.Session = scoped_session(
            sessionmaker(bind=self._engine, expire_on_commit=False, class_=AsyncSession)
        )

    async def create_all_models(self):
        """
        Create all models found in crypto_finder.models module
        """
        for full_module_name in get_package_contents("crypto_finder.models"):
            importlib.import_module(full_module_name)
        async with self._engine.begin() as conn:
            await conn.run_sync(self.BaseModel.metadata.create_all)

    async def close_db_engine(self):
        """
        Dispose DB engine
        """
        self.engine.dispose()


db = DatabaseManager()
