import pytest

from learning_app.calculator import add, divide


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (2, 3, 5),
        (-2, 3, 1),
        (0, 0, 0),
        (1.5, 2.5, 4.0),
    ],
)
def test_add_returns_sum(left: float, right: float, expected: float) -> None:
    assert add(left, right) == expected


@pytest.mark.parametrize(
    ("dividend", "divisor", "expected"),
    [
        (8, 2, 4),
        (-9, 3, -3),
        (1, 4, 0.25),
    ],
)
def test_divide_returns_quotient(
    dividend: float, divisor: float, expected: float
) -> None:
    assert divide(dividend, divisor) == expected


def test_divide_by_zero_raises() -> None:
    with pytest.raises(ZeroDivisionError, match="divisor must not be zero"):
        divide(10, 0)
