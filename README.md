# crypto_finder

[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

| What          | Where                                       |
| ------------- | ------------------------------------------- |
| Documentation | http://localhost:8899/docs                  |
| Maintainer    | [nordzisko](https://github.com/nordzisko)   |

## Crypto Finder aiohttp application

Application that connects to exchanges thru `ccxt` library and obtain prices from cryptocurrency exchange.

Default exchange used in this project is *kucoin*. Base currency is *USDT*.
Both these values can be changes in `docker-compose.yml` file or in `settings.py` as default value.

Docs to this API is accessible on URL `http://localhost:8899/docs` and is done with Swagger.

## Usage

To install & run:

```
docker-compose up
```

Application is exposed on port 8899 and has two endpoints:

- GET `/price/{currency}`
- GET `/price/history?page={page}`

*Postgres* database is exposed on port 5432 and credentials if needed could be found in `config/default.conf` file.
I would strongly suggest storing passwords in some tools for secrets such as Vault,
but it is out of the scope of this project.

### Code formatting

Code formatting is done by [Black formatter](https://github.com/ambv/black/) to format the Python files.

### Pre-commit hooks

Set of pre-commit hooks to apply Black, check YAML and Markdown files, etc. is provided.
You can install `pre-commit` with `pip` or `brew`.
Then you can install hooks itself with command: `pre-commit install --install-hooks` in your repo folder.
