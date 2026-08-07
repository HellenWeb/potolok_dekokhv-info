from __future__ import annotations

import asyncio
import httpx

from admin.bot.config import settings


class ApiClient:
    def __init__(self) -> None:
        self._base_url = settings.API_BASE_URL.rstrip("/")
        self._api_v1 = settings.API_V1_STR.strip("/")

    async def _request(self, method: str, path: str):
        url = f"{self._base_url}/{self._api_v1}/{path.lstrip('/')}"
        last_error: httpx.HTTPError | None = None

        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=20) as client:
                    response = await client.request(method, url)
                    response.raise_for_status()
                    if not response.content:
                        return None
                    return response.json()
            except httpx.HTTPStatusError:
                raise
            except httpx.HTTPError as error:
                last_error = error
                if attempt < 2:
                    await asyncio.sleep(0.4 * (attempt + 1))

        if last_error is not None:
            raise last_error
        return None

    async def get_tasks(self):
        return await self._request("GET", "tasks")

    async def delete_task(self, task_id: int):
        await self._request("DELETE", f"tasks/{task_id}")


api_client = ApiClient()
