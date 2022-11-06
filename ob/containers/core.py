from aiobotocore.session import get_session
from dependency_injector import containers, providers

from ob.factories import ObpyFileFactory
from ob.resources.ddb_client import init_ddb_client
from ob.resources.s3_client import init_s3_client
from ob.settings import Settings
from ob.storage.compressors import DummyCompressor, GzCompressor
from ob.storage.repositories import CloudRepository, FsRepository, UploadsRepository
from ob.use_cases.upload_obpy_file import UploadObpyFile

from .binance import BinanceContainer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Settings()])

    binance = providers.Container(
        BinanceContainer,
        config=config.binance,
    )

    obpy_extension = providers.Object(".obpy")

    obpy_file_factory = providers.Singleton(
        ObpyFileFactory, fs_root=config.storage.fs_root, extension=obpy_extension
    )

    aws_session = providers.Resource(get_session)

    s3_client = providers.Resource(
        init_s3_client,
        session=aws_session,
        region=config.aws_region,
        access_key=config.aws_access_key,
        secret_key=config.aws_secret_key,
    )

    ddb_client = providers.Resource(
        init_ddb_client,
        session=aws_session,
        region=config.aws_region,
        access_key=config.aws_access_key,
        secret_key=config.aws_secret_key,
    )

    gz_compressor = providers.Singleton(GzCompressor, compress_level=5)
    dummy_compressor = providers.Singleton(DummyCompressor)

    cloud_repo = providers.Singleton(
        CloudRepository,
        s3_client=s3_client,
        bucket_name=config.storage.s3_bucket_name,
        compressor=gz_compressor,
        content_type="application/obpy",
    )

    uploads_repo = providers.Singleton(
        UploadsRepository,
        ddb_client=ddb_client,
        table_name=config.storage.uploads_table_name,
    )

    fs_repo = providers.Singleton(
        FsRepository, fs_root=config.storage.fs_root, extension=obpy_extension
    )

    upload_obpy_file = providers.Factory(
        UploadObpyFile,
        obpy_file_factory=obpy_file_factory,
        fs_repo=fs_repo,
        cloud_repo=cloud_repo,
    )
