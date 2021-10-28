"""Custom middleware for aiohttp."""
from typing import Any
import uuid

from aiohttp.web import middleware, Request, Response
import structlog

log = structlog.get_logger()


@middleware
async def logger(request: Request, handler: Any) -> object:
    """
    Add a structlog logger to the request object.

    The logger is accessible like `request["logger"]` later. It will have a
    request ID and some extra info bound to it.
    """
    request["logger"] = log.new(request_id=str(uuid.uuid4()), url=request.path)
    return await handler(request)
