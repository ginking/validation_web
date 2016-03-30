# -*- coding: utf-8 -*-
"""
read/write files for valideer
"""
import os
import json
import validictory
# good alternatives for validictor:
# https://github.com/johnnoone/json-spec   - also implements json-reference
# https://pypi.python.org/pypi/schema      - allows "and" and "or"


def list_schema(path=None):
    """
    get list of all known schema
    """
    if not path:
        path = '../schema'  # XXX: use RW config

    return [os.path.splitext(category)[0] for category in os.listdir(path)]


def list_data(path=None):
    """
    get list of all known schema
    """
    if not path:
        path = '../data'  # XXX: use RW config

    re = {}
    for category in os.listdir(path):
        re[category] = []
        for name in os.listdir(os.path.join(path, category)):
            re[category].append(os.path.splitext(name)[0])
    return re


def validate_data(data_path=None, schema_path=None):
    """
    validate data
    """
    if not data_path:
        data_path = '../data'  # XXX: use RW config

    if not schema_path:
        schema_path = '../schema'  # XXX: use RW config

    data = load_data(data_path)
    schema = load_schema(schema_path)
    re = {}
    for category, values in data.items():
        re[category] = []
        for name, value in values.items():
            try:
                validictory.validate(value, schema[category])
                re[category].append((name, True, None))
            except validictory.validator.ValidationError as e:
                re[category].append((name, False, e.message))
    return re


def load_data(path=None):
    """
    load data from disc
    """
    if not path:
        path = '../data'  # XXX: use RW config
    
    data = {}
    for category in os.listdir(path):
        data[category] = {}
        for filename in os.listdir(os.path.join(path, category)):
            # get name from filename
            name = os.path.splitext(filename)[0]
            
            filename = os.path.join(path, category, filename)
            data[category][name] = json.loads(file(filename, 'r').read())
            
    return data
    
    
def load_schema(path=None):
    """
    load schema from disc
    """
    if not path:
        path = '../schema'  # XXX: use RW config
        
    schema = {}
    for filename in os.listdir(path):
        name = os.path.splitext(filename)[0]
        filename = os.path.join(path, filename)
        schema[name] = json.loads(file(filename, 'r').read())
    return schema


def main():
    global data, schema
    data = load_data()
    schema = load_schema()
    for category, values in data.items():
        for name, value in values.items():
            try:
                validictory.validate(value, schema[category])
                print 'ok', category, name
            except validictory.validator.ValidationError as e:
                print 'error validating {}->{}: {}'.format(
                    category, name, e.message)


if __name__ == '__main__':
    main()
