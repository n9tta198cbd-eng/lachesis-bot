"""
Абстракция источника случайности.

RandomProvider — интерфейс. QRNGOutshiftProvider — рабочая реализация.
Замена провайдера не требует изменений в хендлерах.
"""

import abc
import logging

import aiohttp

logger = logging.getLogger(__name__)

_NUMERIC_KEYS = ("raw", "value", "bits", "data", "number", "numbers",
                 "random_numbers", "result", "output", "block", "integer")


def _extract_bit(obj: object) -> int | None:
    """Рекурсивно ищет первое целое число в произвольной структуре JSON."""
    if isinstance(obj, (int, float)) and not isinstance(obj, bool):
        return int(obj) & 1
    if isinstance(obj, list):
        for item in obj:
            result = _extract_bit(item)
            if result is not None:
                return result
    if isinstance(obj, dict):
        # Сначала — по известным ключам, потом — по всем подряд
        for key in _NUMERIC_KEYS:
            if key in obj:
                result = _extract_bit(obj[key])
                if result is not None:
                    return result
        for val in obj.values():
            result = _extract_bit(val)
            if result is not None:
                return result
    return None


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

                logger.info("QRNG response: %s", data)

                bit = _extract_bit(data)
                if bit is not None:
                    return bit

                raise RuntimeError(f"QRNG: неизвестный формат ответа: {data}")
