from ...match_types import match_types_by_name


def execute(db, params):
    """Execute the query."""
    return {
        "count_distribution": db.matches.get_count_distribution_global(
            match_types_by_name[params["match_type"]]
        )
    }
