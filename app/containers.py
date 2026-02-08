# app/containers.py
from dependency_injector import containers, providers

from app.domain.rank.rank_client import RankClient
from app.domain.rank.repositories.rank_repository import RankRepository
from app.domain.rank.services.rank_service import RankService
from app.common.auth_client import AuthClient
from app.domain.stock.repositories.stock_client import StockClient
from app.domain.stock.repositories.stock_repository import StockRepository
from app.domain.stock.services.stock_service import StockService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["app.api.rank_controller", "app.api.stock_controller"],
    )

    # Clients (Singleton - 토큰 상태 유지)
    auth_client = providers.Singleton(AuthClient)
    rank_client = providers.Singleton(RankClient)
    stock_client = providers.Singleton(StockClient)

    # Repositories
    rank_repository = providers.Factory(
        RankRepository,
        auth_client=auth_client,
        rank_client=rank_client
    )

    stock_repository = providers.Factory(
        StockRepository,
        auth_client=auth_client,
        stock_client=stock_client
    )

    # Services
    rank_service = providers.Factory(
        RankService,
        rank_repository=rank_repository
    )

    stock_service = providers.Factory(StockService, stock_repository=stock_repository)
