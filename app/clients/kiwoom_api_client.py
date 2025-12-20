from app.config import settings
from app.core.exceptions import KiwoomAPIException
from app.models.stock import StockItem, ForeignTradingItem, ForeignTradingResponse
from app.core.logger import logger

class KiwoomApiClient:

    def __init__(self):
        self.base_url = settings.KIWOOM_BASE_URL


    # 종목 정보 리스트
    async def get_stock_llist(self, auth_headers: dict, mrkt_tp: str) -> list[StockItem]:
        import httpx

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "authorization": f"Bearer {auth_headers.get('token')}",
            "api-id": auth_headers.get('api_id')
        }

        url = f"{self.base_url}/api/dostk/stkinfo"
        body = {"mrkt_tp": mrkt_tp}

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=body)
            response.raise_for_status()
            result = response.json()

            raw_list = result.get("list") or []
            stocks: list[StockItem] = []
            for item in raw_list:
                stocks.append(StockItem(**item))
            return stocks


    async def get_stock_trading(self, auth_headers: dict, stock_code: str):
        import httpx
        url = f"{self.base_url}/api/dostk/frgnistt"

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "authorization": f"Bearer {auth_headers.get('token')}",
            "api-id": auth_headers.get('api_id')
        }

        body = {
            "stk_cd": stock_code,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=body)
                response.raise_for_status()

                result = response.json()

                if result.get("return_code") == 0:
                    items = [
                        ForeignTradingItem(**item)
                        for item in result.get('stk_frgnr', [])
                    ]

                    trade_response = ForeignTradingResponse(
                        items=items,
                        total_count=len(items)
                    )

                    logger.info(f"외국인 매매동향 조회 성공: {stock_code}")
                    return trade_response
                else:
                    raise KiwoomAPIException(result.get("return_msg"))

        except httpx.HTTPError as e:
            logger.error(f"API 호출 실패: {str(e)}")
            raise KiwoomAPIException(f"API 호출 실패: {str(e)}")

kiwoom_api_client = KiwoomApiClient()