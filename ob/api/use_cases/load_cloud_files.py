from ob.storage.repositories import UploadsRepository


class LoadCloudFiles:
    def __init__(self, uploads_repo: UploadsRepository):
        self.uploads_repo = uploads_repo

    def call(self, exchange_name, symbol_name):
        return self.uploads_repo.list(
            exchange_name=exchange_name, symbol_name=symbol_name
        )
