from core.reports.query_types import count_distribution

def test_count_distribution_create() -> None:
    x = count_distribution.create(1,2)
    assert x == {
                    'type': count_distribution.TYPE_NAME,
                    'params': {
                        'account': 1,
                        'match_type': 2
                    }
                }