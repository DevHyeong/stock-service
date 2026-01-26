import httpx

from app.config import settings
from app.core.exceptions import AuthenticationException
from app.core.logger import logger


class AuthClient:
    def __init__(self):
        self.base_url = settings.KIWOOM_BASE_URL
        self.appkey = settings.KIWOOM_APPKEY
        self.secretkey = settings.KIWOOM_SECRETKEY
        self._token = None
        self._expires_dt = None


    @property
    def token(self) -> str:
        '''현재 토큰 반환'''
        return self._token

    async def get_token(self) -> dict:
        '''접근 토큰 발급'''
        url = f"{self.base_url}/oauth2/token"

        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }

        data = {
            "grant_type": "client_credentials",
            "appkey": self.appkey,
            "secretkey": self.secretkey
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()

                result = response.json()

                if result.get("return_code") == 0:
                    self._token = result.get("token")
                    self._expires_dt = result.get("expires_dt")

                    logger.info(f"토큰 발급 성공: {self._expires_dt}까지 유효")

                    return {
                        "token": self._token,
                        "expires_dt": self._expires_dt,
                        "token_type": result.get("token_type")
                    }
                else:
                    raise AuthenticationException(result.get("return_msg"))

        except httpx.HTTPError as e:
            logger.error(f"토큰 발급 실패: {str(e)}")
            raise AuthenticationException(f"토큰 발급 실패: {str(e)}")

    async def revoke_token(self) -> dict:
        '''접근 토큰 폐기'''
        if not self._token:
            return {"message": "폐기할 토큰이 없습니다"}

        url = f"{self.base_url}/oauth2/revoke"

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {self._token}"
        }

        data = {
            "appkey": self.appkey,
            "secretkey": self.secretkey,
            "token": self._token
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()

                result = response.json()

                self._token = None
                self._expires_dt = None

                logger.info("토큰 폐기 성공")

                return {"message": result.get("return_msg", "토큰이 폐기되었습니다")}

        except httpx.HTTPError as e:
            logger.error(f"토큰 폐기 실패: {str(e)}")
            raise AuthenticationException(f"토큰 폐기 실패: {str(e)}")

    async def ensure_token(self):
        '''토큰이 없으면 자동 발급'''
        if not self._token:
            await self.get_token()
        return self._token
