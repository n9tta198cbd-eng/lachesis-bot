from dataclasses import dataclass, field
from os import environ

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    qrng_api_key: str
    qrng_url: str = "https://api.qrng.outshift.com/api/v1/random_numbers"
    qrng_timeout: float = 8.0


def load_config() -> Config:
    token = environ.get("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN не задан в .env")

    qrng_key = environ.get("QRNG_API_KEY", "").strip()
    if not qrng_key:
        raise RuntimeError("QRNG_API_KEY не задан в .env")

    return Config(bot_token=token, qrng_api_key=qrng_key)
