from aiobotocore.session import get_session
from dependency_injector import containers, providers

from ob.exchanges.binance import BinanceExchange
from ob.factories import ObpyFileFactory
from ob.storage.compressors import DummyCompressor, GzCompressor
from ob.storage.repositories import CloudRepository, FsRepository
from ob.resources.s3 import init_s3

from .binance import BinanceContainer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["./config.ini"])

    obpy_extension = providers.Object(".obpy")

    obpy_file_factory = providers.Singleton(
        ObpyFileFactory, fs_root=config.storage.fs_root, extension=obpy_extension
    )

    aws_session = providers.Resource(get_session)

    s3 = providers.Resource(
        init_s3,
        session=aws_session,
        region=config.aws_region,
        access_key=config.aws_access_key,
        secret_key=config.aws_secret_key,
    )

    gz_compressor = providers.Singleton(GzCompressor, compress_level=6)
    dummy_compressor = providers.Singleton(DummyCompressor)

    cloud_repo = providers.Singleton(
        CloudRepository,
        s3=s3,
        bucket_name=config.storage.s3_bucket,
        compressor=gz_compressor,
        content_type="application/obpy",
    )

    fs_repo = providers.Singleton(
        FsRepository, fs_root=config.storage.fs_root, extension=obpy_extension
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
