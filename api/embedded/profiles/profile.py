import json

memory_path = None

memory = None

"""
Base memory:
{
    files: {}
}
"""


def load():
    global memory_path, memory
    file = open(memory_path)
    memory = json.load(file)
    file.close()
    if 'files' not in memory:
        raise ValueError("Memory path is bad")


def save():
    global memory_path, memory
    file = open(memory_path, "w+")
    json.dump(memory, file)
    file.close()


def setup(_memory_path):
    global memory_path
    memory_path = _memory_path
    load()


def get_file_obj(file_name):
    global memory
    if file_name in memory["files"]:
        return memory["files"][file_name]
    memory["files"][file_name] = {
        "File Name": file_name,
        "Processed": False,
        "Last Order": "No Last Order"
    }
    return memory["files"][file_name]


prep_order = None


def get_orders(available_files):
    global memory

    orders = []

    for file in available_files:
        file_obj = get_file_obj(file)
        if not file_obj["Processed"]:
            # TODO: If it started running already, don't run it again
            order = prep_order(file)
            file_obj["Last Order"] = order
            if order is not None:
                orders.append(order)
    save()
    return orders


def cb_running(order):
    file_obj = get_file_obj(order["File Name"])
    file_obj["Started Running"] = True
    save()


def cb_processed(order):
    file_obj = get_file_obj(order["File Name"])
    file_obj["Processed"] = True
    save()
