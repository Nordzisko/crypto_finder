import asynctest


class SessionFixture:
    def __init__(self, *args, target_mock: asynctest.MagicMock = None, **kwargs):
        self._session = asynctest.MagicMock(name="transactional_session_mock")

    async def __aenter__(self, *args, **kwargs):
        return self._session

    async def __aexit__(self, exc_type, exc, tb, *args, **kwargs):
        pass
