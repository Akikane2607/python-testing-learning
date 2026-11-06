import requests
import pytest

from learning_app.user_api import fetch_user


def test_fetch_user_returns_user(
    requests_mock, sample_user: dict[str, object]
) -> None:
    requests_mock.get("https://example.test/users/7", json=sample_user)

    result = fetch_user("https://example.test/", 7)

    assert result == sample_user
    assert requests_mock.last_request.method == "GET"
    assert requests_mock.last_request.qs == {}


def test_fetch_user_uses_request_timeout(mocker) -> None:
    response = mocker.Mock()
    response.json.return_value = {"id": 7, "name": "Lin"}
    get = mocker.patch("learning_app.user_api.requests.get", return_value=response)

    fetch_user("https://example.test", 7)

    get.assert_called_once_with("https://example.test/users/7", timeout=5)


@pytest.mark.parametrize("user_id", [0, -1, True, 1.5, "7"])
def test_fetch_user_rejects_invalid_user_id(user_id: object) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        fetch_user("https://example.test", user_id)  # type: ignore[arg-type]


def test_fetch_user_raises_for_http_error(requests_mock) -> None:
    requests_mock.get("https://example.test/users/7", status_code=404)

    with pytest.raises(requests.HTTPError):
        fetch_user("https://example.test", 7)


def test_fetch_user_raises_for_timeout(requests_mock) -> None:
    requests_mock.get(
        "https://example.test/users/7",
        exc=requests.exceptions.Timeout,
    )

    with pytest.raises(requests.exceptions.Timeout):
        fetch_user("https://example.test", 7)


def test_fetch_user_rejects_invalid_json(requests_mock) -> None:
    requests_mock.get(
        "https://example.test/users/7",
        text="not-json",
        headers={"Content-Type": "application/json"},
    )

    with pytest.raises(ValueError, match="valid JSON"):
        fetch_user("https://example.test", 7)


@pytest.mark.parametrize(
    "response_data",
    [
        [],
        {"id": 7},
        {"id": "7", "name": "Lin"},
        {"id": 8, "name": "Lin"},
        {"id": 7, "name": None},
    ],
)
def test_fetch_user_rejects_invalid_response_shape(
    requests_mock, response_data: object
) -> None:
    requests_mock.get("https://example.test/users/7", json=response_data)

    with pytest.raises(ValueError, match="invalid user shape"):
        fetch_user("https://example.test", 7)
