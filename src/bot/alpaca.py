from __future__ import annotations

from typing import Any

from .config import Settings
from .http_client import request_json


class AlpacaSafetyError(RuntimeError):
    pass


class AlpacaClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    @property
    def headers(self) -> dict[str, str]:
        return {
            "APCA-API-KEY-ID": self.settings.alpaca_api_key,
            "APCA-API-SECRET-KEY": self.settings.alpaca_secret_key,
        }

    def _url(self, path: str) -> str:
        return self.settings.alpaca_base_url + path

    def assert_paper(self) -> None:
        if not self.settings.is_paper:
            raise AlpacaSafetyError(
                "Live trading is blocked. Use ALPACA_ENV=paper, paper base URL, and LIVE_TRADING_ENABLED=false."
            )

    def account(self) -> dict[str, Any]:
        return request_json("GET", self._url("/v2/account"), headers=self.headers)

    def positions(self) -> list[dict[str, Any]]:
        data = request_json("GET", self._url("/v2/positions"), headers=self.headers)
        return data if isinstance(data, list) else []

    def asset(self, symbol: str) -> dict[str, Any]:
        return request_json("GET", self._url(f"/v2/assets/{symbol}"), headers=self.headers)

    def place_market_notional_order(self, symbol: str, notional: float) -> dict[str, Any]:
        self.assert_paper()
        payload = {
            "symbol": symbol,
            "notional": f"{notional:.2f}",
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
        }
        return request_json("POST", self._url("/v2/orders"), headers=self.headers, payload=payload)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

