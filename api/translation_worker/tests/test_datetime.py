import pytest
from ..all_to_unix import all_to_unix
from ..exceptions import ExecutionException


def test_datetime():
    assert all_to_unix("2/3/2021 4:5:6 PM") == 1612368306
    assert all_to_unix("2/3/2021") == 1612310400
    assert all_to_unix("") is None
    assert all_to_unix("2019-03-15T01:02:03") == 1552611723
    assert all_to_unix("false") is None
    assert all_to_unix(" False") is None
    assert all_to_unix(" Talse") is None
    assert all_to_unix(" NULL") is None
    assert all_to_unix("null") is None
    assert all_to_unix("  -  -  ") is None
    assert all_to_unix("12/31/9999 23:59:59") is None
    assert all_to_unix("12/31/9999") is None

    with pytest.raises(ExecutionException):
        all_to_unix("2/2/2050")

    with pytest.raises(ExecutionException):
        all_to_unix("2/2/1700")
