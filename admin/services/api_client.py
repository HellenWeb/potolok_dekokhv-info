from __future__ import annotations

import httpx

from admin.bot.config import settings


class ApiClient:
    def __init__(self) -> None:
        self._base_url = settings.API_BASE_URL.rstrip("/")
        self._api_v1 = settings.API_V1_STR.strip("/")

    async def _request(self, method: str, path: str):
        url = f"{self._base_url}/{self._api_v1}/{path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.request(method, url)
            response.raise_for_status()
            return response.json()

    async def get_tasks(self):
        return await self._request("GET", "tasks")

    async def get_reviews(self):
        return await self._request("GET", "reviews")


api_client = ApiClient()

