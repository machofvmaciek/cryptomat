"""Module gathering views for viewer app."""
import json

from typing import Any

# from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from modules.mock_api import generate_n_records

def __format_coin_data(coins_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Limits decimal places in fields of coins dicts."""
    formatted = []
    for coin in coins_data:
        formatted_coin = {}
        for name, details in coin.items():
            formatted_coin[name] = {
                "current_price": round(details["current_price"], 2),
                "ath": round(details["ath"], 2),
                "change_24": round(details["change_24"], 2)
            }
        formatted.append(formatted_coin)

    return formatted

def index(request: HttpRequest) -> HttpResponse:
    """Index page of viewer."""

    records = json.loads(generate_n_records())

    data = []
    for coin_name in records:
        data.append({coin_name: records[coin_name]})

    # formatted_data = __
    context = {
        "coins_data": __format_coin_data(data)
    }

    return render(request, "index.html", context=context)
