from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, TEXT, NUMERIC
from sqlalchemy.future import select

from crypto_finder.database import db, DatabaseManager
from crypto_finder.settings import HISTORY_PAGE_SIZE

import structlog

__all__ = [
    "Currency",
]

logger = structlog.get_logger()


class Currency(db.BaseModel):
    """
    Data model for currencies DB table.
    """

    __tablename__ = "currencies"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    currency = Column(TEXT, nullable=False)
    date_ = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    price = Column(NUMERIC, nullable=False)

    def __init__(
        self,
        id_: int = None,
        currency: str = None,
        date: datetime = None,
        price: Decimal = None,
    ):
        """
        New model instance initializer

        :param id_: id of the example, it will default to None, because it is auto-generated in DBv
        :param currency
        :param date
        :param price
        """
        self.id = id_
        self.currency = currency
        self.date_ = date
        self.price = price

    async def insert_price_to_db(self, db_manager: DatabaseManager):
        """
        Insert self object into database and commits operation

        :param db_manager: Database manager which creates session
        """
        async with db_manager.Session() as session:
            async with session.begin():
                session.add(self)
                await session.commit()

    @classmethod
    async def get_currency_history(
        cls, db_manager: DatabaseManager, page_index: int
    ) -> List[Dict[str, Any]]:
        """
        Get history records from database of given page index

        :param db_manager: Database manager which creates session
        :param page_index: Page index obtained thru API
        :return: list of serialized history records
        """
        async with db_manager.Session() as session:
            async with session.begin():
                raw_records = await session.execute(
                    select(Currency)
                    .limit(HISTORY_PAGE_SIZE)
                    .offset((page_index - 1) * HISTORY_PAGE_SIZE)
                )
                serialized_records = [
                    raw_record[0].serialize() for raw_record in raw_records
                ]
                return serialized_records

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize record to Dict

        @return serialized record
        """
        return {
            "id": str(self.id) if self.id else None,
            "currency": self.currency,
            "price": self.price,
            "timestamp": self.date_.astimezone(timezone.utc).isoformat(),
        }
