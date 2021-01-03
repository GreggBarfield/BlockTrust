from flask import g

def unauth(params):
    return auth(params)

def auth(params):
    return {
        'count_eid_distinct': g.db.matches.get_count_eid_distinct()
    }
