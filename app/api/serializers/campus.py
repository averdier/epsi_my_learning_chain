# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


campus_resource = api.model('Campus resource model', {
    'id': fields.String(required=True, description='Campus ID'),
    'name': fields.String(required=True, description='Campus name'),
})

campus_container = api.model('Campus container', {
    'campus': fields.List(fields.Nested(campus_resource), required=True, description='Campus list')
})
