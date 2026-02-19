import logging
from typing import List

from app.common.api_client import ApiClient
from app.common.kiwoom_api_path import INVESTOR_DAILY_TRADE_STOCK_PATH
from app.config import settings
from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStockRequest, InvestorDailyTradeResponse, \
    InvestorDailyTradeStock


class StockClient:

    def __init__(self):
        self.base_url = settings.KIWOOM_BASE_URL

    # 투자자별 일별 매매 종목 요청
    async def get_investor_daily_trade_stock(
        self,
        access_token: str,
        investorDailyTradeStockRequest: InvestorDailyTradeStockRequest
    ) -> List[InvestorDailyTradeStock]:

        headers = {
            "api-id": "ka10058",
            "authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        api = ApiClient(
            base_url=self.base_url,
            default_headers=headers,
        )

        response = await api._request(
            method= "POST",
            path= INVESTOR_DAILY_TRADE_STOCK_PATH,
            response_model=InvestorDailyTradeResponse,
            json=investorDailyTradeStockRequest.model_dump(exclude_none=True)
        )

        return response.invsr_daly_trde_stk

