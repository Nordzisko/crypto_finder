"""
Routes module.

Responsible for providing the means to register the application routes.
"""
from crypto_finder.controllers.currency_api import CurrencyApiController
from crypto_finder.controllers.ping import PingController


def setup_routes(app):
    ping_controller = PingController()
    currency_api_controller = CurrencyApiController()

    # API ROUTES
    # used for public endpoints
    app.router.add_get("/price/history", currency_api_controller.get_currency_history)
    app.router.add_get("/price/{currency}", currency_api_controller.get_currency_price)

    # INTERNAL API ROUTES
    # used for health checks and ping
    app.router.add_get("/ping", ping_controller.ping)
