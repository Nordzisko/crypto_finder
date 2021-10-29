from datetime import datetime, timezone
from decimal import Decimal

from crypto_finder.models.currency import Currency


async def test_currency_serializer():
    currency = "BTC"
    date = datetime(2021, 11, 11, 11, 11, 0).replace(tzinfo=timezone.utc)
    price = Decimal("10.21")

    currency_obj = Currency(currency=currency, date=date, price=price)

    serialized = currency_obj.serialize()
    assert float(serialized["price"]) == 10.21
    assert serialized["timestamp"] == "2021-11-11T11:11:00+00:00"
    assert serialized["currency"] == currency
