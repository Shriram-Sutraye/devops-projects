# test_calculator.py - Unit tests for the calculator

import sys
sys.path.insert(0, 'src')

from calculator import add, subtract, multiply, divide
import pytest

# ============================================
# ADDITION TESTS
# ============================================
def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_add_mixed_numbers():
    assert add(-1, 5) == 4

# ============================================
# SUBTRACTION TESTS
# ============================================
def test_subtract_positive():
    assert subtract(10, 4) == 6

def test_subtract_negative_result():
    assert subtract(4, 10) == -6

# ============================================
# MULTIPLICATION TESTS
# ============================================
def test_multiply_positive():
    assert multiply(3, 4) == 12

def test_multiply_by_zero():
    assert multiply(5, 0) == 0

# ============================================
# DIVISION TESTS
# ============================================
def test_divide_positive():
    assert divide(20, 4) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

# ============================================
# RUN MESSAGE
# ============================================
if __name__ == "__main__":
    print("Run with: pytest tests/test_calculator.py -v")
