from dependency_injector import containers, providers

from ob.api.use_cases import LoadCloudFiles

from .core import Container


class ApiContainer(containers.DeclarativeContainer):

    core = providers.Container(Container)

    wiring_config = containers.WiringConfiguration(
        modules=[
            "ob.api.routers.cloud",
        ]
    )

    load_cloud_files = providers.Factory(LoadCloudFiles, uploads_repo=core.uploads_repo)
