from aiohttp.web import HTTPBadRequest, HTTPRequestTimeout
from datetime import datetime as dt
from decimal import Decimal
from typing import Tuple

import ccxt.async_support as ccxt
from ccxt.base.exchange import Exchange
from ccxt.base.errors import BadSymbol, ExchangeNotAvailable, RequestTimeout
import structlog

from crypto_finder.settings import DATE_FORMAT, DEFAULT_BASE_CURRENCY, DEFAULT_EXCHANGE

logger = structlog.get_logger()


class ExchangeClient:
    def __init__(self, exchange=DEFAULT_EXCHANGE, base_currency=DEFAULT_BASE_CURRENCY):
        self.base_currency = base_currency
        if exchange in ccxt.exchanges:
            self.exchange = exchange
        else:
            self.exchange = DEFAULT_EXCHANGE
            logger.error(
                "Selected exchange is not supported, falling back to KuCoin exchange!"
            )

    def create_exchange_session(self) -> Exchange:
        """
        Create Exchange session for communication with specific exchage in async mode
        @return: Exchange
        """
        class_from_ccxt = getattr(ccxt, self.exchange)
        exchange_object = class_from_ccxt()
        return exchange_object

    async def get_last_bid_info(
        self, currency: str, limit: int = 20
    ) -> Tuple[Decimal, dt]:
        """
        Function for communication with exchange, obtain order book with last bids and asks
        Set correct types needed later in applicationn

        @param currency: Currency for which fetch order book with bids
        @param limit: Limit of bids and asks obtained from exchange
        @return: Last bid value and its timestamp
        """
        symbol = f"{currency}/{self.base_currency}"

        async with self.create_exchange_session() as session:
            # Kucoin exchange that was in example seemed to be accessible publicly only with limit 20 or 100
            # Reference: https://github.com/ccxt/ccxt/blob/1.59.2/python/ccxt/kucoin.py#L960
            try:
                bid_data = await session.fetch_order_book(symbol, limit=limit)
            except BadSymbol as e:
                reason = f"Bad Request: {e.args[0]}"
                raise HTTPBadRequest(reason=reason)
            except (RequestTimeout, ExchangeNotAvailable):
                raise HTTPRequestTimeout(
                    reason="Exchange timeout or not available at the moment"
                )

            # Convert float to string and then to Decimal for more exact storing in Numeric datatype in PG
            last_bid = Decimal(str(bid_data["bids"][0][0]))
            timestamp = dt.strptime(session.iso8601(bid_data["timestamp"]), DATE_FORMAT)
            return last_bid, timestamp
