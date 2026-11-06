"""Business logic that uses the user API client."""

from typing import Any

from learning_app.user_api import fetch_user


def get_user_label(base_url: str, user_id: int) -> str:
    """Return a short label for a user."""
    user: dict[str, Any] = fetch_user(base_url, user_id)
    return f"{user['name']} (#{user['id']})"
