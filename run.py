from aiohttp import web
from crypto_finder.app import create_app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=8899)
