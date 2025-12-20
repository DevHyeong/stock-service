from app.clients.kiwoom_api_client import kiwoom_api_client
from app.config import settings
from app.services.auth_service import auth_service


class StockService:
    def __init__(self):
        self.base_url = settings.KIWOOM_BASE_URL

    async def get_stock_list(self):
        token = await auth_service.ensure_token()

        return await kiwoom_api_client.get_stock_llist(
            auth_headers={
                "token": token,
                "api_id": "ka10099"
            },
            mrkt_tp="0"
        )

stock_service = StockService()