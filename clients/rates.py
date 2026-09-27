from clients.http import (
    ExternalServiceError,
    ResourceNotFoundError,
    get_json,
)

RATE_URL = "https://api.frankfurter.dev/v2/rate/{currency}/RUB"


def get_rate(currency: str) -> float:
    currency = currency.upper()

    try:
        data = get_json(
            RATE_URL.format(currency=currency),
        )
    except ResourceNotFoundError as error:
        raise ResourceNotFoundError(
            f"Currency not found: {currency}"
        ) from error

    rate = data.get("rate")

    if rate is None:
        raise ExternalServiceError(
            f"Invalid rate response for currency: {currency}"
        )

    try:
        return float(rate)
    except (TypeError, ValueError) as error:
        raise ExternalServiceError(
            "Invalid rate value"
        ) from error
