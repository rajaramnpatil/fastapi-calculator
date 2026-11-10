import pytest

from app.operations import add, divide, multiply, subtract


@pytest.mark.parametrize(
    ("operation", "a", "b", "expected"),
    [
        (add, 2, 3, 5),
        (add, -2.5, 3, 0.5),
        (subtract, 5, 3, 2),
        (subtract, 2.5, 4, -1.5),
        (multiply, 2, 3, 6),
        (multiply, -2.5, 4, -10),
        (divide, 6, 3, 2),
        (divide, 5.5, 2, 2.75),
    ],
)
def test_arithmetic_operations(operation, a, b, expected):
    assert operation(a, b) == pytest.approx(expected)


def test_divide_by_zero():
    with pytest.raises(ValueError, match=r"^Cannot divide by zero!$"):
        divide(5, 0)