from aiohttp import web
from aiohttp_apispec import use_kwargs
import structlog

from crypto_finder.controllers.base import BaseJsonApiController
from crypto_finder.models.currency import Currency
from crypto_finder.schemas import HistoryRequestSchema

logger = structlog.get_logger()

DEFAULT_PAGE = "1"


class CurrencyApiController(BaseJsonApiController):
    async def get_currency_price(self, request: web.Request) -> web.Response:
        """
        Function gets last bid from exchange defined in exchange client and returns obtained data

        :param web.Request request: aiohttp web request
        :return web.Reponse instance with last bid data of given currency along with timestamp of the price
        """
        currency = request.match_info["currency"]

        exchange_client = request.app["exchange_client"]
        last_bid, timestamp = await exchange_client.get_last_bid_info(currency)

        currency_record = Currency(currency=currency, date=timestamp, price=last_bid)
        await currency_record.insert_price_to_db(request.app["db_manager"])

        serialized_record = currency_record.serialize()
        return self.json_response(
            body={
                "price": serialized_record["price"],
                "timestamp": serialized_record["timestamp"],
            }
        )

    @use_kwargs(HistoryRequestSchema, locations=["query"])
    async def get_currency_history(self, request: web.Request) -> web.Response:
        """
        Function gets paginated history of the database records of all historically obtianed currency bids
        along with the timestamp. There is page number present in query parameter, which is first checked
        against schema.

        :param web.Request request: aiohttp web request
        :return web.Reponse instance with history data of given page ordered descending by timestamp
        """
        page_index = int(request.query.get("page", DEFAULT_PAGE))
        currency_history = await Currency.get_currency_history(
            request.app["db_manager"], page_index
        )
        return self.json_response(body={"data": currency_history})
