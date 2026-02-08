import httpx
from typing import Dict, Any, Optional
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class ApiClient:
    def __init__(
        self,
        base_url: str,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: float = 5.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.default_headers = default_headers or {}
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.default_headers,
            timeout=timeout,
        )

    async def _request(
        self,
        method: str,
        path: str,
        response_model: Type[T],
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> T:
        try:
            response = await self.client.request(
                method=method,
                url=path,
                params=params,
                json=json,
                headers=headers,
            )
            response.raise_for_status()
            return response_model.model_validate(response.json())

        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"HTTP {e.response.status_code}: {e.response.text}"
            ) from e

        except httpx.RequestError as e:
            raise RuntimeError(f"Request failed: {str(e)}") from e

    def request_list(
        self,
        method: str,
        path: str,
        response_model: Type[T],
        params: Optional[Dict[str, Any]] = None,
    ) -> list[T]:
        try:
            response = self.client.request(
                method=method,
                url=path,
                params=params,
            )
            response.raise_for_status()
            return [
                response_model.model_validate(item)
                for item in response.json()
            ]

        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"HTTP {e.response.status_code}: {e.response.text}"
            ) from e

    def close(self):
        self.client.close()