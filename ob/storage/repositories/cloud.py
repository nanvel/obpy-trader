from aiobotocore.client import BaseClient

from ..compressors import BaseCompressor


class CloudRepository:
    def __init__(
        self,
        s3_client: BaseClient,
        bucket_name: str,
        compressor: BaseCompressor,
        content_type: str,
    ):
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.compressor = compressor
        self.content_type = content_type

    async def upload(self, source_path, target_path):
        with open(source_path, "rb") as f:
            extra_params = {
                "ContentEncoding": self.compressor.encoding,
            }
            extra_params = {k: v for k, v in extra_params.items() if v is not None}

            await self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=self.compressor.rename(target_path),
                Body=self.compressor.call(f),
                ContentType=self.content_type,
                **extra_params,
            )
