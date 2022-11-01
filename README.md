# Order Book Trading Framework

Plan:
- ui
- start new file after certain number of rows
- move dd table to configs in pulumi
- analytics / logs
- create iam role for the app (pulumi)
- order book visualizer
- time factory
- usage from jupyter
- extend tests
- build and deploy in docker
- skip updates outside order book / reload when shifted 25%
- obpy restarts when connection lost
- refactor storage to fs first and upload to s3 + records in pg (coverage)
- build candles from trades
- dashboard to pull and upload data sets

600kb / minute -> 160kb zip.
9mb/15min -> 2.4mb zip / 15min.

## Development

```console
brew install poetry
poetry install
poetry shell
obpy --help
```
