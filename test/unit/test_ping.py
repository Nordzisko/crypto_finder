from crypto_finder.controllers.ping import PingController


async def test_ping(mocker):
    request = mocker.MagicMock()

    response = await PingController().ping(request)
    assert response.text == '{"pong": true}'
