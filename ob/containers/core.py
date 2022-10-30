from aiobotocore.session import get_session
from dependency_injector import containers, providers

from ob.exchanges.binance import BinanceExchange
from ob.storage.compressors import GzCompressor
from ob.storage.repositories import CloudRepository
from ob.storage.use_cases.build_file_path import BuildFilePath
from ob.resources.s3 import init_s3

from .binance import BinanceContainer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["./config.ini"])

    build_file_path = providers.Singleton(
        BuildFilePath, prefix=config.storage.fs_root, extension=".obpy"
    )

    aws_session = providers.Resource(get_session)

    s3 = providers.Resource(
        init_s3,
        session=aws_session,
        region=config.aws_region,
        access_key=config.aws_access_key,
        secret_key=config.aws_secret_key,
    )

    compressor = providers.Singleton(GzCompressor, compress_level=6)

    cloud_repository = providers.Singleton(
        CloudRepository,
        s3=s3,
        bucket_name=config.storage.s3_bucket,
        compressor=compressor,
    )

    binance_exchange = providers.Factory(
        BinanceExchange,
        base_url="https://api.binance.com",
        symbol_factory=BinanceContainer.symbol_factory,
        order_book_factory=BinanceContainer.order_book_factory,
        order_book_updates_factory=BinanceContainer.order_book_updates_factory,
        trade_factory=BinanceContainer.trade_factory,
        stream=BinanceContainer.binance_stream,
    )
