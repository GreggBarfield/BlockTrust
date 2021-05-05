import pytest
from ..blocks import block_eid_from_animal_id
from ....exceptions import ExecutionException


def test_block_non_int():
    with pytest.raises(ExecutionException):
        block_eid_from_animal_id("", 3)


def test_block_int():
    assert block_eid_from_animal_id(53, "asg4w4we") == "MFA:ANEID:53:asg4w4we"
