"""The main app module, with the app and routing configuration."""
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from aiohttp import ClientSession, web
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware
from aiohttp_swagger import setup_swagger
from pathlib import Path, PurePath
import structlog

from crypto_finder import middleware, settings
from crypto_finder.config import get_config
from crypto_finder.database import db
from crypto_finder.routes import setup_routes
from crypto_finder.services.exchange import ExchangeClient


logger = structlog.get_logger()


async def client_session_ctx(app: web.Application):
    """
    Aiohttp app context preparing `ClientSession` with User-Agent header.
    """

    default_headers = {"User-Agent": settings.USER_AGENT}
    app["session"] = ClientSession(headers=default_headers)
    yield
    await app["session"].close()


async def on_app_startup(app: web.Application):
    """
    Defines the on-startup signal behavior for the application. The app parameter is
      important for aiohttp's Signal interface.

    :param app: The application instance the signal is being executed for.
    """
    host = app["config"].get("server", "host")
    port = app["config"].get("server", "port")
    logger.info(f"Starting up crypto_finder on address: {host}:{port}...")

    # Initialize database engine
    app["db_manager"] = db
    app["db_manager"].init_db_engine()
    await app["db_manager"].create_all_models()

    # Initialize Exchange Client
    app["exchange_client"] = ExchangeClient(exchange="kucoin")

    # Started!
    logger.info(f"crypto_finder successfully started on {host}:{port}!")


async def on_app_cleanup(app: web.Application):
    """
    Defines the on-cleanup signal behavior for the application. The app parameter is
      important for aiohttp's Signal interface.

    :param app: The application instance the signal is being executed for.
    """
    # Cleaning up...
    logger.info("Cleaning up crypto_finder's resources...")

    # Clean up the database resources
    await app["db_manager"].close_db_engine()

    # Cleaned up!
    logger.info("crypto_finder's resources were successfully cleaned up!")


async def on_app_shutdown():
    logger.info("Shutting down crypto_finder...")


def create_app() -> web.Application:
    # Initialize web Application
    app = web.Application(middlewares=[middleware.logger, validation_middleware])

    # Load config file
    app["config"] = get_config()

    app.on_startup.append(on_app_startup)
    app.on_cleanup.append(on_app_cleanup)

    # Setup Routes
    setup_routes(app)

    # Setup Swagger
    this_modules_path = Path(__file__).parent.absolute()
    api_swagger_doc_path = str(PurePath(this_modules_path, "docs/swagger-v1.0.yaml"))
    setup_swagger(app, swagger_url="/docs", swagger_from_file=api_swagger_doc_path)
    setup_aiohttp_apispec(app, swagger_path="/docs")

    app.cleanup_ctx.append(client_session_ctx)
    return app


# gunicorn requires async function for creating app
async def create_app_async():
    return create_app()
