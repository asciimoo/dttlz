import json as _json
import pickle as _pickle
import csv as _csv
from StringIO import StringIO


def load_json(json_string, **kwargs):
    return _json.loads(json_string, **kwargs)


def load_json_file(json_filename, **kwargs):
    with open(json_filename, 'r') as json_file:
        return _json.load(json_file, **kwargs)


def dump_json(obj, **kwargs):
    return _json.dumps(obj, **kwargs)


def dump_json_file(obj, filename, **kwargs):
    with open(filename, 'wb') as outfile:
        return _json.dump(obj, outfile, **kwargs)


def load_pickle(pickle_string):
    return _pickle.loads(pickle_string)


def load_pickle_file(pickle_filename):
    with open(pickle_filename, 'rb') as pickle_file:
        return _pickle.load(pickle_file)

def dump_pickle(obj):
    return _pickle.dumps(obj)


def dump_pickle_file(obj, filename):
    with open(filename, 'wb') as outfile:
        return _pickle.dump(obj, outfile)


def _parse_csv_file(fp, delimiter=',', quotechar='"', header=True):
    fp.seek(0)
    parser = _csv.DictReader(fp, delimiter=delimiter, quotechar=quotechar)
    data = []
    for x in parser:
        data.append(x)
    return data

def load_csv(csv_string, **kwargs):
    csv_stringio = StringIO()
    csv_stringio.write(csv_string)
    return _parse_csv_file(csv_stringio, **kwargs)


def load_csv_file(csv_filename, **kwargs):
    with open(csv_filename, 'rb') as csv_file:
        return _parse_csv_file(csv_file, **kwargs)


def dump_csv_file(obj, filename, **kwargs):
    with open(filename, 'wb') as outfile:
        writer = _csv.DictWriter(outfile, **kwargs)
        if type(obj) == list:
            writer.writerows(obj)
        elif type(obj) == dict:
            for key, data in obj.items():
                data['_id'] = key
                writer.writerow(data)

def dump_csv(obj, **kwargs):
    out = StringIO()
    dump_csv_file(obj, out, **kwargs)
    out.seek(0)
    return out.read()
