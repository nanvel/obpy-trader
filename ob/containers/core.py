from dependency_injector import containers, providers

from ob.exchanges.service import ExchangesService


class Container(containers.DeclarativeContainer):
    auth_service = providers.Factory(ExchangesService, exchanges=[])
