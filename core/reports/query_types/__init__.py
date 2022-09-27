types = {}

from . import count_eid_distinct  # noqa
types[count_eid_distinct.TYPE_NAME] = count_eid_distinct

from . import count_distribution_global  # noqa
types[count_distribution_global.TYPE_NAME] = count_distribution_global

from . import count_distribution  # noqa
types[count_distribution.TYPE_NAME] = count_distribution

from . import count_eid_distinct_by_account  # noqa
types[count_eid_distinct_by_account.TYPE_NAME] = count_eid_distinct_by_account

from . import market_data_cache  # noqa
types[market_data_cache.TYPE_NAME] = market_data_cache

from . import count_distribution_for_sector_at_account  # noqa
types[count_distribution_for_sector_at_account.TYPE_NAME] = count_distribution_for_sector_at_account

from . import sustainability_response_averages  # noqa
types[sustainability_response_averages.TYPE_NAME] = sustainability_response_averages
