types = {}

from . import count_eid_distinct  # noqa
types[count_eid_distinct.TYPE_NAME] = count_eid_distinct

from . import count_distribution_global  # noqa
types[count_distribution_global.TYPE_NAME] = count_distribution_global

from . import count_distribution  # noqa
types[count_distribution.TYPE_NAME] = count_distribution

from . import count_eid_distinct_by_account  # noqa
types[count_eid_distinct_by_account.TYPE_NAME] = count_eid_distinct_by_account
