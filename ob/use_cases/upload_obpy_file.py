from ob.factories.obpy_file import ObpyFileFactory
from ob.storage.repositories.fs import FsRepository
from ob.storage.repositories.cloud import CloudRepository


class UploadObpyFile:
    def __init__(
        self,
        obpy_file_factory: ObpyFileFactory,
        fs_repo: FsRepository,
        cloud_repo: CloudRepository,
    ):
        self.obpy_file_factory = obpy_file_factory
        self.fs_repo = fs_repo
        self.cloud_repo = cloud_repo

    async def call(self, fs_path: str, remove_file: bool):
        obpy_file = self.obpy_file_factory.from_path(fs_path)

        assert not obpy_file.is_temp

        await self.cloud_repo.upload(
            source_path=obpy_file.fs_path, target_path=obpy_file.cloud_path
        )

        if remove_file:
            self.fs_repo.remove(obpy_file.fs_path)
