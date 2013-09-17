from operator import itemgetter


def index(data, idx):
    ret = {}
    for row in data:
        idx_value = row[idx]
        ret.setdefault(idx_value, {}).update({x:y for x,y in row.items() if x != idx})

    return ret


def multi_index(data, indexes):
    ret = {}
    for row in data:
        idx = tuple(row.pop(index) for index in indexes)
        ret[idx] = row

    return ret


def merge(*datas):
    ret = {}
    for data in datas:
        for idx,row in data.items():
            ret.setdefault(idx,{}).update(row)

    return ret


def get_rows(data, indexes):
    ret = {}
    getters = [itemgetter(x) for x in indexes]
    for k,row in data:
        new_row = {}
        for gi,getter in enumerate(getters):
            new_row[indexes[gi]] = getter(row)
        ret[k] = new_row

    return ret
