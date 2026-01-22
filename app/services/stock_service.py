from app.clients.kiwoom_api_client import kiwoom_api_client
from app.config import settings
from app.models.stock import Stock
from app.repositories.stock_repository import StockRepository
from app.services.auth_service import auth_service


class StockService:
    def __init__(self, repo: StockRepository) :
        self.base_url = settings.KIWOOM_BASE_URL
        self.repo = repo

    async def get_stock_list(self):
        token = await auth_service.ensure_token()

        response = await kiwoom_api_client.get_stock_llist(
            auth_headers={
                "token": token,
                "api_id": "ka10099"
            },
            mrkt_tp="0"
        )

        stock_list = response.get('output', []) if isinstance(response, dict) else response

        # 3. DTO → Entity 변환
        stocks = [
            Stock(
                code=item.code,
                name=item.name,
                list_count=item.listCount,
                audit_info=item.auditInfo,
                reg_day=item.regDay,
                last_price=item.lastPrice,
                state=item.state,
                market_code=item.marketCode,
                market_name=item.marketName,
                up_name=item.upName,
                up_size_name=item.upSizeName,
                company_class_name=item.companyClassName,
                order_warning=item.orderWarning,
                nxt_enable=item.nxtEnable
            )
            for item in stock_list
        ]

        # 4. bulk insert (await 필수!)
        saved_stocks = await self.repo.save_all(stocks)

        return saved_stocks

