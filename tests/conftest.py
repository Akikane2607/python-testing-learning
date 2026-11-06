import pytest


@pytest.fixture
def sample_user() -> dict[str, object]:
    return {"id": 7, "name": "Lin"}
