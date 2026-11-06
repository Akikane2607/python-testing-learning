"""A small HTTP client used to practice isolated API tests."""

from typing import Any

import requests


def fetch_user(base_url: str, user_id: int) -> dict[str, Any]:
    """Fetch one user and validate the shape of the JSON response."""
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id < 1:
        raise ValueError("user_id must be a positive integer")

    url = f"{base_url.rstrip('/')}/users/{user_id}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise ValueError("response must contain valid JSON") from error

    if (
        not isinstance(data, dict)
        or not isinstance(data.get("id"), int)
        or not isinstance(data.get("name"), str)
        or data["id"] != user_id
    ):
        raise ValueError("response has an invalid user shape")

    return data
