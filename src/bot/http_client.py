from __future__ import annotations

import json
from typing import Any
from urllib import error, request


class HttpClientError(RuntimeError):
    pass


def request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: int = 30,
) -> Any:
    body = None
    req_headers = {"Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        req_headers["Content-Type"] = "application/json"

    req = request.Request(url=url, data=body, headers=req_headers, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            text = response.read().decode("utf-8")
            return json.loads(text) if text else {}
    except error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        raise HttpClientError(f"{method} {url} failed with {exc.code}: {response_body}") from exc
    except error.URLError as exc:
        raise HttpClientError(f"{method} {url} failed: {exc}") from exc

