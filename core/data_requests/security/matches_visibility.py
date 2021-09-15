def apply_visibility(matches, allow_account_ids=()):
    """Applies visibility to matches.

    Params:
        matches: A list of matches
        allow_accounts: A list of allowed account IDs to bypass visibility settings
    Returns:
        A tuple of two lists, visible matches and blocked matches, with blocked
            matches being
                {
                    'id':
                    'type':
                    'partner_account':
                    'visibility':
                }
            with eid notably missing
    """
    visible_matches = []
    blocked_matches = []

    for match in matches:
        if match['visibility'] is True or match['partner_account'] in allow_account_ids:
            visible_matches.append(match)
        else:
            blocked_matches.append(
                {
                    'id': match['id'],
                    'type': match['type'],
                    'account': match['partner_account'],
                    'visibility': match['visibility']
                }
            )

    return visible_matches, blocked_matches
