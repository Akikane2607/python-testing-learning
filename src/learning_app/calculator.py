"""Simple functions for practicing unit tests."""


def add(left: float, right: float) -> float:
    """Return the sum of two numbers."""
    return left + right


def divide(dividend: float, divisor: float) -> float:
    """Divide one number by another."""
    if divisor == 0:
        raise ZeroDivisionError("divisor must not be zero")
    return dividend / divisor
