from calculation import multiple
import pytest

# @pytest.mark.slow
def test_add():
    assert 2+2 == 4

def test_multiple():
    assert multiple(3, 4) == 12

def test_multiple_with_zero():
    assert multiple(10, 0) == 0
    