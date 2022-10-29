# Order Book Trading Framework

Plan:
- load obpy
- order book visualizer
- time factory
- usage from jupyter
- extend tests
- build and deploy in docker
- skip updates outside order book / reload when shifted 25%
- obpy restarts when connection lost
- rotate files to s3
- refactor storage to fs first and upload to s3 + records in pg (coverage)
- build candles from trades
- dashboard to pull and upload data sets

## Development

```console
brew install poetry
poetry install
poetry shell
```
