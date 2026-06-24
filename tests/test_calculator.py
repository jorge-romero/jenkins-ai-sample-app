"""Tests for calculator module.

BUG #5: Test that triggers division by zero bug!
"""
import pytest
from src.calculator import Calculator


def test_add():
    """Test addition (this one is correct)."""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0


def test_subtract():
    """Test subtraction (this one is correct)."""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(0, 5) == -5


def test_divide_normal():
    """Test normal division (this one is correct)."""
    calc = Calculator()
    assert calc.divide(10, 2) == 5
    assert calc.divide(7, 2) == 3.5


def test_divide_by_zero():
    """Test division by zero.
    
    This test asserts that a ValueError is raised when attempting to divide by zero.
    """
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)


def test_get_first_n_items_normal():
    """Test getting first N items normally (this one is correct)."""
    calc = Calculator()
    items = ["a", "b", "c", "d", "e"]
    assert calc.get_first_n_items(items, 3) == ["a", "b", "c"]
    assert calc.get_first_n_items(items, 1) == ["a"]


def test_get_first_n_items_edge_case():
    """Test getting more items than exist.
    
    BUG #5: This test will FAIL due to off-by-one error in the implementation!
    When n > len(items), the function returns items[0:n-1] instead of all items.
    """
    calc = Calculator()
    items = ["a", "b", "c"]
    # OBVIOUS BUG: Should return all 3 items, but function returns only 2!
    result = calc.get_first_n_items(items, 10)
    assert len(result) == 3  # Expects 3, but gets 2!
    assert result == ["a", "b", "c"]  # This will fail!
