from __future__ import annotations

import time
from typing import Optional

import requests


class ExternalServiceError(Exception):
    """Ошибка внешнего сервиса."""


class ResourceNotFoundError(ExternalServiceError):
    """Ресурс не найден."""


def get_json(
    url: str,
    params: Optional[dict] = None,
    timeout: float = 10.0,
    retries: int = 2,
) -> dict:
    last_error: Optional[Exception] = None

    for attempt in range(retries + 1):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=timeout,
            )

            if response.status_code == 404:
                raise ResourceNotFoundError(
                    "Resource not found"
                )

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")

                if retry_after and retry_after.isdigit() and attempt < retries:
                    time.sleep(int(retry_after))
                    continue

                raise ExternalServiceError(
                    f"Too Many Requests: {response.status_code}"
                )

            if response.status_code in {500, 502, 503, 504}:
                if attempt < retries:
                    time.sleep(1)
                    continue

                raise ExternalServiceError(
                    f"External service error: {response.status_code}"
                )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):
                raise ExternalServiceError(
                    "External service returned invalid JSON format"
                )

            return data

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ) as error:
            last_error = error

            if attempt < retries:
                time.sleep(1)
                continue

            raise ExternalServiceError(
                "External service is unavailable"
            ) from error

        except requests.exceptions.JSONDecodeError as error:
            raise ExternalServiceError(
                "External service returned invalid JSON"
            ) from error

    raise ExternalServiceError(
        "External service is unavailable"
    ) from last_error
