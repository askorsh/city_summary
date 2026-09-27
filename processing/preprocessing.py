def preprocess_weather(weather: dict) -> dict:
    result = dict(weather)

    temperature = result.get("temp_c")

    result["warm_clothes"] = (
        isinstance(temperature, (int, float))
        and temperature < 0
    )

    return result


def preprocess_rate(rate_data: dict) -> dict:
    result = dict(rate_data)

    rate = result.get("rate_to_rub")

    result["expensive"] = (
        isinstance(rate, (int, float))
        and rate > 100
    )

    return result
