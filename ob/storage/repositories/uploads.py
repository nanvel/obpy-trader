from aiobotocore.client import BaseClient


class UploadsRepository:
    def __init__(self, ddb_client: BaseClient, table_name: str):
        self.ddb_client = ddb_client
        self.table_name = table_name

    async def list(self, exchange_name, symbol_name):
        response = await self.ddb_client.query(
            TableName=self.table_name,
            KeyConditionExpression="ExchangeSymbol = :es",
            ExpressionAttributeValues={":es": {"S": f"{exchange_name}:{symbol_name}"}},
            Limit=100,
            ScanIndexForward=False,
        )

        # {'Items': [{'TsStart': {'N': '1667219043852'}, 'Size': {'N': '60781'}, 'TsStop': {'N': '1667219052148'}, 'Exchange': {'S': 'binance'}, 'Symbol': {'S': 'BTCUSDT'}, 'ExchangeSymbol': {'S': 'binance:BTCUSDT'}, 'Bucket': {'S': 'obpy-90093b2'}, 'Key': {'S': 'binance/BTCUSDT/2022-10-31/1667219043852_1667219052148.obpy'}}], 'Count': 1, 'ScannedCount': 1, 'ResponseMetadata': {'RequestId': '0K5K64RHNK2NLQKK7DMBKVDGHJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Sun, 06 Nov 2022 08:02:54 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '321', 'connection': 'keep-alive', 'x-amzn-requestid': '0K5K64RHNK2NLQKK7DMBKVDGHJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '1217290581'}, 'RetryAttempts': 0}}

        return [self._parse_item(i) for i in response["Items"]]

    @staticmethod
    def _parse_item(item: dict):
        res = {}
        for k, tv in item.items():
            for kt, v in tv.items():
                if kt == "N":
                    res[k] = int(v)
                else:
                    res[k] = v
        return res
