from crypto_finder.controllers.base import BaseJsonApiController


class PingController(BaseJsonApiController):
    async def ping(self, request):
        """
        Return a response saying ``{"pong": true}``.

        This is useful for testing and health checks.
        """
        return self.json_response({"pong": True})
