def execute(db, params):
    """Execute the query."""
    return {
        'count_eid_distinct': db.matches.get_count_eid_distinct()
    }
