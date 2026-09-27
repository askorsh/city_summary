from clients.http import (
    ExternalServiceError,
    ResourceNotFoundError,
    get_json,
)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city: str) -> dict:
    geocoding_data = get_json(
        GEOCODING_URL,
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )

    results = geocoding_data.get("results")

    if not isinstance(results, list) or not results:
        raise ResourceNotFoundError(f"City not found: {city}")

    location = results[0]

    latitude = location.get("latitude")
    longitude = location.get("longitude")

    if latitude is None or longitude is None:
        raise ExternalServiceError("Invalid geocoding response")

    weather_data = get_json(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code",
            "temperature_unit": "celsius",
        },
    )

    current = weather_data.get("current")

    if not isinstance(current, dict):
        raise ExternalServiceError("Invalid weather response")

    temperature = current.get("temperature_2m")
    weather_code = current.get("weather_code")

    if temperature is None or weather_code is None:
        raise ExternalServiceError("Weather data is incomplete")

    return {
        "temp_c": float(temperature),
        "description": _weather_description(int(weather_code)),
    }


def _weather_description(weather_code: int) -> str:
    descriptions = {
        0: "clear sky",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "fog",
        48: "depositing rime fog",
        51: "light drizzle",
        53: "moderate drizzle",
        55: "dense drizzle",
        61: "slight rain",
        63: "moderate rain",
        65: "heavy rain",
        71: "slight snow",
        73: "moderate snow",
        75: "heavy snow",
        80: "slight rain showers",
        81: "moderate rain showers",
        82: "violent rain showers",
        95: "thunderstorm",
        96: "thunderstorm with slight hail",
        99: "thunderstorm with heavy hail",
    }

    return descriptions.get(weather_code, "unknown weather")
