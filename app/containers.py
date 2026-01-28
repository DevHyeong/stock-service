# app/containers.py
from dependency_injector import containers, providers

from app.domain.rank import RankClient
from app.domain.rank.repositories.rank_repository import RankRepository
from app.domain.rank.services.rank_service import RankService
from app.common.auth_client import AuthClient


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["app.api.rank_controller"]
    )

    # Clients (Singleton - 토큰 상태 유지)
    auth_client = providers.Singleton(AuthClient)
    rank_client = providers.Singleton(RankClient)

    # Repositories
    rank_repository = providers.Factory(
        RankRepository,
        auth_client=auth_client,
        rank_client=rank_client
    )

    # Services
    rank_service = providers.Factory(
        RankService,
        rank_repository=rank_repository
    )
