def generate_insert(
    account, insert_namespace, insert_type, fields,
    insert_id=None, block=None, status=0, priority=0, created=None
):
    """

    Params:
        created: If None, might be autoconfigured
    """
    return {
        "id": insert_id,
        "account": account,
        "namespace": insert_namespace,
        "type": insert_type,
        "fields": fields,
        "status": status,
        "priority": priority,
        "block": block,
        "row": None,
    }
