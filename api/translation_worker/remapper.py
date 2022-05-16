from copy import deepcopy


def remap(d, plan):
    for k, v in plan.items():
        if k in d and v in d:
            raise ValueError("Remap failed horribly (new key already exists)! 1")

    result = deepcopy(d)

    for d_key in d.keys():
        if d_key in plan:
            if plan[d_key] in result:
                raise ValueError("Remap failed horribly (new key already exists)! 2")
            result[plan[d_key]] = d[d_key]
    return result
