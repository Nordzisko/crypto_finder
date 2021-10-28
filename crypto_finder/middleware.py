"""Custom middleware for aiohttp."""
import uuid

from aiohttp.web import middleware
import structlog

log = structlog.get_logger()


@middleware
async def logger(request, handler):
    """
    Add a structlog logger to the request object.

    The logger is accessible like `request["logger"]` later. It will have a
    request ID and some extra info bound to it.
    """
    request["logger"] = log.new(request_id=str(uuid.uuid4()), url=request.path)
    return await handler(request)
