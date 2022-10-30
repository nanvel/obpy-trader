class CloudRepository:
    def __init__(self, s3, bucket_name, compressor):
        self.s3 = s3
        self.bucket_name = bucket_name
        self.compressor = compressor

    async def upload(self, source_path, target_path):
        with open(source_path, "r") as f:
            await self.s3.put_object(
                Bucket=self.bucket_name,
                Key=self.compressor.rename(target_path),
                Body=self.compressor.call(f),
            )
