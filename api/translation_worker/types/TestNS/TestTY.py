def block_key(insert):
    if insert['account'] >= 0:
        raise RuntimeError("Not allowed to TestTY")
    if 'key' in insert['fields']:
        return insert['fields']['key']
    return None


def handle(db, inserts_model, insert, block_value):
    print(insert)
    if 'emit' in insert['fields'] and 'emit_key' in insert['fields']:
        return [(insert['fields']['emit_key'], insert['fields']['emit'])]
    return []
