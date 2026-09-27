from clients.rates import get_rate
from clients.weather import get_weather
from processing.preprocessing import preprocess_rate, preprocess_weather


def build_city_summary(city: str, currency: str = "USD") -> dict:
    weather = get_weather(city)
    weather = preprocess_weather(weather)

    rate_data = {
        "currency": currency.upper(),
        "rate_to_rub": get_rate(currency),
    }
    rate_data = preprocess_rate(rate_data)

    return {
        "city": city,
        "weather": weather,
        "rate": rate_data,
    }
