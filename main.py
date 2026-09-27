import argparse
import json
import sys

from clients.http import ExternalServiceError, ResourceNotFoundError
from processing.service import build_city_summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Сводка по городу",
    )

    parser.add_argument(
        "--city",
        default="Moscow",
        help="Название города",
    )

    parser.add_argument(
        "--currency",
        default="USD",
        help="Код валюты ISO",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывести результат в JSON",
    )

    return parser.parse_args()


def print_summary(summary: dict) -> None:
    weather = summary["weather"]
    rate = summary["rate"]

    print(f"Город: {summary['city']}")
    print(
        f"Погода: {weather['temp_c']}°C, "
        f"{weather['description']}"
    )
    print(
        "Тёплая одежда: "
        f"{'да' if weather['warm_clothes'] else 'нет'}"
    )
    print(
        f"Курс {rate['currency']} → RUB: "
        f"{rate['rate_to_rub']:.2f}"
    )
    print(
        "Дорогой курс: "
        f"{'да' if rate['expensive'] else 'нет'}"
    )


def main() -> int:
    args = parse_args()

    try:
        summary = build_city_summary(
            args.city,
            args.currency,
        )
    except ResourceNotFoundError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 3
    except ExternalServiceError as error:
        print(f"Ошибка внешнего сервиса: {error}", file=sys.stderr)
        return 4

    if args.json:
        print(
            json.dumps(
                summary,
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print_summary(summary)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
