from aiobotocore.session import Session
from aiobotocore.client import BaseClient


async def init_ddb_client(
    session: Session, region: str, access_key: str | None, secret_key: str | None
) -> BaseClient:
    async with session.create_client(
        "dynamodb",
        region_name=region,
        aws_secret_access_key=access_key,
        aws_access_key_id=secret_key,
    ) as client:
        yield client
