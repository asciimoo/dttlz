# -*- coding: utf-8 -*-

"""
dttlz.io
~~~~~~~~

This module implements the dttlz io functions.

"""
"""
:copyright: (c) 2013 by Adam Tauber.
:license: AGPL, see LICENSE for more details.

"""

import json as _json
import pickle as _pickle
import csv as _csv
import os
import fcntl
import termios
import struct
from StringIO import StringIO

def _getTerminalSize():
    """get terminal width,height
    according to http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python"""
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

def show(data):
    """displays list of dicts formatted"""
    # TODO list of lists
    width, height = _getTerminalSize()
    if not len(data):
        return
    headers = data[0].keys()
    colsize = width/len(headers)-7
    colwidths = {}
    for row in data[:height-2]:
        for rowname,rowvalue in row.items():
            colwidths[rowname] = min(colsize, max(len(str(rowvalue)), colwidths.get(rowname, 0)))
    print headers
    print ',-' + '---'.join('-'*(colwidths[rowname]) for rowname in headers) + '-.'
    print '| ' + ' | '.join(str(rowname)[:colsize].ljust(colwidths[rowname]) for rowname in headers) + ' |'
    print '|-' + '-+-'.join('-'*(colwidths[rowname]) for rowname in headers) + '-|'
    for row in data[:height-2]:
        print '| ' + ' | '.join(str(col)[:colsize].ljust(colwidths[rowname]) for rowname,col in row.items()) + ' |'


def load_json(json_string, **kwargs):
    """loads a json string to python object

    kwargs passed to json.loads"""
    return _json.loads(json_string, **kwargs)


def load_json_file(json_filename, **kwargs):
    """loads a json file to python object

    kwargs passed to json.load"""
    with open(json_filename, 'r') as json_file:
        return _json.load(json_file, **kwargs)


def dump_json(obj, **kwargs):
    """python object to json string

    kwargs passed to json.dumps"""
    return _json.dumps(obj, **kwargs)


def dump_json_file(obj, filename, **kwargs):
    """python object to json file

    kwargs passed to json.dump"""
    with open(filename, 'wb') as outfile:
        return _json.dump(obj, outfile, **kwargs)


def load_pickle(pickle_string):
    """loads a pickle string to python object"""
    return _pickle.loads(pickle_string)


def load_pickle_file(pickle_filename):
    """loads a pickle file to python object"""
    with open(pickle_filename, 'rb') as pickle_file:
        return _pickle.load(pickle_file)

def dump_pickle(obj):
    """python object to pickle string"""
    return _pickle.dumps(obj)


def dump_pickle_file(obj, filename):
    """python object to pickle file"""
    with open(filename, 'wb') as outfile:
        return _pickle.dump(obj, outfile)


def parse_csv(fp, typedict=None, **kwargs):
    """parses csv file with DictReader

    typedict defines row types (format: {'rowname': type})
    kwargs passed to csv.DictReader"""
    parser = _csv.DictReader(fp, **kwargs)
    data = []
    for x in parser:
        if typedict:
            for rowname,rowtype in typedict.items():
                x[rowname] = rowtype(x[rowname])
        data.append(x)
    return data

def load_csv(csv_string, **kwargs):
    """loads a csv string to python dict

    kwargs passed to parse_csv"""
    csv_stringio = StringIO()
    csv_stringio.write(csv_string)
    csv_stringio.seek(0)
    return parse_csv(csv_stringio, **kwargs)


def load_csv_file(csv_filename, **kwargs):
    """loads a csv file to python dict

    kwargs passed to parse_csv"""
    with open(csv_filename, 'rb') as csv_file:
        return parse_csv(csv_file, **kwargs)


def dump_csv_file(obj, filename, **kwargs):
    """python list/dict to csv file"""
    with open(filename, 'wb') as outfile:
        writer = _csv.DictWriter(outfile, **kwargs)
        if type(obj) == list:
            writer.writerows(obj)
        elif type(obj) == dict:
            for key, data in obj.items():
                data['_id'] = key
                writer.writerow(data)

def dump_csv(obj, **kwargs):
    """python list/dict to csv string"""
    out = StringIO()
    dump_csv_file(obj, out, **kwargs)
    out.seek(0)
    return out.read()
