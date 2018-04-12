# -*- coding: utf-8 -*-

from flask_restplus import fields
from .nested import file_nested, project_nested
from .iota import iota_address_model, api


campus_post_model = api.model('Campus POST model', {
    'name': fields.String(required=True, min_length=4, description='Campus name'),
    'description': fields.String(required=False, description='Campus description')
})

campus_patch_model = api.model('Campus PATCH model', {
    'name': fields.String(required=False, min_length=4, description='Campus name'),
    'description': fields.String(required=False, description='Campus description')
})

campus_minimal_model = api.model('Campus minimal model', {
    'id': fields.String(required=True, description='Campus ID'),
    'name': fields.String(required=True, description='Campus name')
})

campus_model = api.inherit('Campus model', campus_minimal_model, {
    'description': fields.String(required=True, description='Campus description')
})

campus_full_model = api.inherit('Campus full model', campus_model, {
    'balance': fields.Integer(required=True, description='Campus balance'),
    'deposit_address': fields.Nested(iota_address_model, required=True, description='Campus deposit address'),
    'files': fields.List(fields.Nested(file_nested), required=True, description='Files list'),
    'projects': fields.List(fields.Nested(project_nested), required=True, description='Projects list')
})

campus_container = api.model('Campus container model', {
    'campus': fields.List(fields.Nested(campus_minimal_model))
})
