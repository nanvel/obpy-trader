# Order Book Trading Framework

Plan:
- api to fetch from ddb
- ui - show uploaded
- deploy
- schedule exchange/symbol
- add liquidations to data
- start new file after certain number of rows
- Amazon EMR for studies (https://www.youtube.com/watch?v=fC4Y7KNwRzs)
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

UI: https://www.naiveui.com/

```console
brew install poetry
poetry install
poetry shell
obpy --help
```
