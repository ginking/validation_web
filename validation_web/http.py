# -*- coding: utf-8 -*-
"""
server for valideer web interface
"""
import rw.http
import rw.routing

from validation import list_schema, load_data, validate_data, load_schema
from . import http_schema
from rw_rest.model import Rest, Model
from rw_rest.provider import FileProvider

root = rw.http.Module('validation_web')
data_root = rw.http.Module('validation_web', 'http_data')
root.mount('/data', data_root)

data_rest = Rest(module=data_root)
for category in list_schema(path='schema'):
    provider = FileProvider('data/'+category)
    data_rest.add_model(
        model=Model(
            provider=provider,
            name=category))

schema_rest = Rest(module=root)
schema_rest.add_model(model=http_schema.Schema(data_rest=data_rest))


@root.get('/')
def main(handler):
    """show main page"""
    handler['schema'] = list_schema('schema')
    handler['data'] = validate_data(data_path='data', schema_path='schema')
    root.render_template("main.html")

