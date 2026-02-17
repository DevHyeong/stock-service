from app.clients.kiwoom_api_client import kiwoom_api_client
from app.config import settings
from app.models.stock import Stock
from app.repositories.stock_repository import StockRepository
from app.services.auth_service import auth_service
from app.schemas.stock import StockResponse, StockListResponse


class StockService:
    def __init__(self, repo: StockRepository) :
        self.base_url = settings.KIWOOM_BASE_URL
        self.repo = repo

    async def get_stock_list(self, skip: int = 0, limit: int = 100, market_code: str = None):
        """DB에서 종목 리스트 조회

        Args:
            skip: 건너뛸 개수
            limit: 조회할 개수
            market_code: 시장구분 (0: KOSPI, 1: KOSDAQ)

        Returns:
            종목 리스트와 전체 개수
        """
        stocks = await self.repo.get_all(skip=skip, limit=limit, market_code=market_code)
        total = await self.repo.count_all(market_code=market_code)

        # Stock 모델을 StockResponse 스키마로 변환
        stock_responses = [StockResponse.model_validate(stock) for stock in stocks]

        return StockListResponse(
            stocks=stock_responses,
            total=total,
            skip=skip,
            limit=limit
        )

    async def sync_stock_list(self, market_code: str = "0"):
        """키움 API에서 종목 리스트를 가져와 DB에 동기화

        Args:
            market_code: 시장구분 (0: KOSPI, 1: KOSDAQ, 전체는 빈 문자열)

        Returns:
            동기화된 종목 수
        """
        token = await auth_service.ensure_token()

        print(f"token: {token}")
        response = await kiwoom_api_client.get_stock_llist(
            auth_headers={
                "token": token,
                "api_id": "ka10099"
            },
            mrkt_tp=market_code
        )

        print(f"response: {response}")

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

        return {
            "synced_count": len(saved_stocks),
            "market_code": market_code
        }


    # 투자자별일별매매종목요청
