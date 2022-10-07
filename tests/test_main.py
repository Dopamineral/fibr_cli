import pytest
from src.main import do_thing


@pytest.mark.parametrize("a,b,c,expected,is_error",
                         [
                             (1, 1, 1, "1.0", False),
                             (1, 0, 1, ZeroDivisionError, True)

                         ])
def test_do_thing(a, b, c, expected, is_error):
    if is_error:
        with pytest.raises(expected):
            do_thing(a, b, c)
    else:

        assert do_thing(a, b, c) == expected
