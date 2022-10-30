import json


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
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
