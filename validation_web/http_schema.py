# -*- coding: utf-8 -*-
"""
add/edit/remove schema using the REST API
"""
import os
import tornado.web
from rw_rest.model import Model
from rw_rest.provider import FileProvider


class Schema(Model):
    def __init__(self, data_rest, data_dir='data'):
        self.data_rest = data_rest
        self.data_dir = data_dir
        self.name = 'schema'
        super(Schema, self).__init__(
            provider=FileProvider(self.name),
            name=self.name)

    def post(self, data):
        os.mkdir(os.path.join(*[self.data_dir, data['name']]))
        category = str(data['name'])
        provider = FileProvider('data/'+category)
        self.data_rest.add_model(
            model=Model(
                provider=provider,
                name=category))
        return super(Schema, self).post(data)

    def delete(self, _id):
        data_dir = os.path.join(*[self.data_dir, _id])
        if os.listdir(data_dir):
            raise tornado.web.HTTPError(404)
        os.remove(data_dir)
        self.data_rest.remove_model(_id)
        return super(Schema, self).delete(_id)