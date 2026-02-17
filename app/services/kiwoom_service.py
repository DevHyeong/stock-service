from app.clients.kiwoom_api_client import kiwoom_api_client
from app.services.auth_service import auth_service


class KiwoomService:
    '''키움 API 서비스'''

    async def get_foreign_trading(
            self,
            stock_code: str,
            date: str = None,
            direction: str = "0"
    ) -> dict:
        '''주식외국인종목별매매동향 조회 (ka10008)'''

        # 토큰 확보
        token = await auth_service.ensure_token()

        return await kiwoom_api_client.get_stock_trading(
            auth_headers={
                "token": token,
                "api_id": "ka10008"
            },
            stock_code=stock_code,
        )

    async def get_multiple_stocks_trading(self, stock_codes: list[str]) -> dict:
        '''여러 종목의 외국인 매매동향 동시 조회'''
        import asyncio

        tasks = [
            self.get_foreign_trading(code)
            for code in stock_codes
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            code: result if not isinstance(result, Exception) else str(result)
            for code, result in zip(stock_codes, results)
        }


    async def get_execution_info(self, stock_code: str) -> dict:
        '''체결정보 조회 (ka10003)'''
        token = await auth_service.ensure_token()

        return await kiwoom_api_client.get_execution_info(
            auth_headers={"token": token},
            stock_code=stock_code
        )


    async def get_bid_ask(self, stock_code: str) -> dict:
        '''호가정보 조회 (ka10004)'''
        token = await auth_service.ensure_token()

        return await kiwoom_api_client.get_bid_ask(
            auth_headers={"token": token},
            stock_code=stock_code
        )


# 싱글톤 인스턴스
kiwoom_service = KiwoomService()