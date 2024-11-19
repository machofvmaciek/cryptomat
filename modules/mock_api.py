"""Module implementing functionalities that act as an API for early stage development."""
import json

from random import random, randint

def generate_n_records(number: int=20) -> str:
    """Return number of foo-like records in json format, mimicking api."""

    records = {}
    for i in range(number):
        records[f"coin_{i}"] = {
            "current_price": random() * 20,
            "ath": 1000,
            "change_24": random() * 10 if randint(0, 10) % 2 == 0 else random() * (-10),
        }

    return json.dumps(records)
