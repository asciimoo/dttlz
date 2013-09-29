# -*- coding: utf-8 -*-

"""
dttlz.model
~~~~~~~~~~~

This module implements the dttlz model functions.

"""
"""
:copyright: (c) 2013 by Adam Tauber.
:license: AGPL, see LICENSE for more details.

"""

from operator import itemgetter

def index(data, idx):
    """indexing list lists/dicts by a single column"""
    ret = {}
    for row in data:
        idx_value = row[idx]
        ret.setdefault(idx_value, {}).update({x:y for x,y in row.items() if x != idx})

    return ret


def multi_index(data, indexes):
    """indexing list lists/dicts by a multiple columns"""
    ret = {}
    for row in data:
        idx = tuple(row.pop(index) for index in indexes)
        ret[idx] = row

    return ret


def merge_dicts(*datas):
    """merging dicts by keys"""
    ret = {}
    for data in datas:
        for idx,row in data.items():
            ret.setdefault(idx,{}).update(row)

    return ret


def get_rows(data, indexes):
    """filtering rows by indexes"""
    ret = {}
    getters = [itemgetter(x) for x in indexes]
    for k,row in data:
        new_row = {}
        for gi,getter in enumerate(getters):
            new_row[indexes[gi]] = getter(row)
        ret[k] = new_row

    return ret

def sort(data, key):
    """sorting list of lists/dicts"""
    return sorted(data, key=itemgetter(key))


