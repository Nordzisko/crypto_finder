"""Application settings that get initialized at startup based on environment variables."""

import os

APP_NAME = "crypto_finder"
DEBUG = os.getenv("CRYPTO_FINDER_DEBUG") == "1"
PACKAGE_VERSION = os.getenv("PACKAGE_VERSION") or "dev"
USER_AGENT = os.getenv("USER_AGENT", f"{APP_NAME}/{PACKAGE_VERSION}")

# Application settings
HISTORY_PAGE_SIZE = int(os.getenv("HISTORY_PAGE_SIZE", "20"))
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
DEFAULT_EXCHANGE = os.getenv("DEFAULT_EXCHANGE", "kucoin")
DEFAULT_BASE_CURRENCY = os.getenv("DEFAULT_BASE_CURRENCY", "USDT")
