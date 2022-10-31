import botocore.session


TABLE_NAME = "obpyTable-3830810"


session = botocore.session.get_session()


def lambda_handler(event, context):
    """
    {
      "Records": [
        {
          "awsRegion": "ap-southeast-1",
          "eventName": "ObjectCreated:Put",
          "s3": {
            "bucket": {
              "name": "obpy-90093b2",
              "arn": "arn:aws:s3:::obpy-90093b2"
            },
            "object": {
              "key": "binance/BTCUSDT/2022-10-30/1667124809.obpy.gz",
              "size": 63101,
              "eTag": "1a860a14acc93b6b7a8cfeb20ae9c7e0",
            }
          }
        }
      ]
    }
    """
    if not event["Records"]:
        return

    region = event["Records"][0]["awsRegion"]
    ddb_client = session.create_client("dynamodb", region_name=region)

    for record in event["Records"]:
        assert record["eventName"] == "ObjectCreated:Put"

        bucket_name = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        size = record["s3"]["object"]["size"]

        *_, exchange, symbol, date_str, file_name = key.split("/")
        file_name, extension = file_name.split(".")
        ts_start, ts_stop = file_name.split("_")

        exchange_symbol = f"{exchange}:{symbol}"

        ddb_client.put_item(
            TableName=TABLE_NAME,
            Item={
                "Bucket": {"S": bucket_name},
                "Key": {"S": key},
                "Exchange": {"S": exchange},
                "Symbol": {"S": symbol},
                "ExchangeSymbol": {"S": exchange_symbol},
                "TsStart": {"N": ts_start},
                "TsStop": {"N": ts_stop},
                "Size": {"N": f"{size}"},
            },
        )

    return {"success": True}
