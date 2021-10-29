from datetime import datetime, timezone
from decimal import Decimal
from unittest import mock

import asynctest

from test.fixtures.database import SessionFixture


@asynctest.patch("crypto_finder.services.exchange.ExchangeClient.get_last_bid_info")
@asynctest.patch("crypto_finder.database.DatabaseManager.Session")
async def test_get_prices(session, get_last_bid, client):
    """
    Example test for integration testing of API endpoint with mocked database session and exchange function.

    :param session: mocked session
    :param get_last_bid: mocked function get_last_bid
    :param client: configured client
    """

    session_mock = mock.MagicMock(name="session_mock")
    session.return_value = SessionFixture(target_mock=session_mock)
    get_last_bid.return_value = (
        Decimal("60422.7"),
        datetime(2021, 11, 11, 11, 11, 11).replace(tzinfo=timezone.utc),
    )

    response = await client.get("/price/BTC")

    assert response.status == 200
    json_response = await response.json()
    assert isinstance(json_response, dict)
    assert json_response["price"] == 60422.7
    assert json_response["timestamp"] == "2021-11-11T11:11:11+00:00"
