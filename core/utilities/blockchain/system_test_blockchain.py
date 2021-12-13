import pytest
from datetime import datetime, timedelta, timezone
from .blockchain_helper import check, transmit
from random import randint


def test_full():
    base_rand = randint(0, 10000000000)
    cases = [
        ["469g8sj09e48gj" + str(base_rand), "gshe4908hwse04g9sej4f9se8ruvjh"],
        ["469g8sj09e48gj" + str(base_rand)]
    ]

    real_record_id = None

    for data in cases:
        start = datetime.now(timezone.utc)
        record_id = transmit(data)
        end = datetime.now(timezone.utc)
        assert abs(end - start) < timedelta(seconds=5)
        for h in data:
            fetch = check(h, record_id)
            assert abs(datetime.now(timezone.utc) - fetch) < timedelta(minutes=10)

        real_record_id = record_id

    fetch = check("gs48gjes4iges4tshdrio5uhgder5g", real_record_id)
    assert fetch is False

    with pytest.raises(Exception):
        fetch = check(cases[0][0], "h498jed4yse4g98sej4gerhd")
        assert fetch is False

    with pytest.raises(Exception):
        fetch = check("g89sej4980gje4", "h498jed4yse4g98sej4gerhd")
        assert fetch is False
