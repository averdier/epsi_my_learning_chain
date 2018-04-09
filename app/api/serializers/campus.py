# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


campus_post_model = api.model('Campus POST model', {
    'name': fields.String(required=True, min_length=4, description='Campus name')
})

campus_put_model = api.inherit('Campus PUT model', campus_post_model, {})

campus_resource = api.model('Campus resource model', {
    'id': fields.String(required=True, description='Campus ID'),
    'name': fields.String(required=True, description='Campus name')
})

campus_container = api.model('Campus container', {
    'campus': fields.List(fields.Nested(campus_resource), required=True, description='Campus list')
})
