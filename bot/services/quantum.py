"""
Абстракция источника случайности.

RandomProvider — интерфейс. QRNGOutshiftProvider — рабочая реализация.
Замена провайдера не требует изменений в хендлерах.
"""

import abc
import logging

import aiohttp

logger = logging.getLogger(__name__)


class RandomProvider(abc.ABC):
    @abc.abstractmethod
    async def get_bit(self) -> int:
        """Вернуть 0 или 1. Поднять RuntimeError если источник недоступен."""


class QRNGOutshiftProvider(RandomProvider):
    """Outshift QRNG API — физический квантовый шум."""

    def __init__(self, api_key: str, url: str, timeout: float = 8.0) -> None:
        self._api_key = api_key
        self._url = url
        self._timeout = timeout

    async def get_bit(self) -> int:
        payload = {
            "encoding": "raw",
            "format": "all",
            "bits_per_block": 1,
            "number_of_blocks": 1,
        }
        headers = {
            "Content-Type": "application/json",
            "x-id-api-key": self._api_key,
        }
        timeout = aiohttp.ClientTimeout(total=self._timeout)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self._url, json=payload, headers=headers, timeout=timeout
            ) as resp:
                body = await resp.text()
                if resp.status != 200:
                    raise RuntimeError(f"QRNG HTTP {resp.status}: {body}")

                try:
                    data = await resp.json(content_type=None)
                except Exception as exc:
                    raise RuntimeError(
                        f"QRNG: ошибка парсинга JSON: {exc}; body={body}"
                    ) from exc

                logger.debug("QRNG response: %s", data)

                # Перебираем возможные ключи в ответе
                for key in (
                    "raw", "data", "random_numbers", "numbers",
                    "result", "value", "bits", "output",
                ):
                    if key in data:
                        val = data[key]
                        if isinstance(val, list) and val:
                            return int(val[0]) & 1
                        if isinstance(val, (int, float)):
                            return int(val) & 1

                raise RuntimeError(f"QRNG: неизвестный формат ответа: {data}")
