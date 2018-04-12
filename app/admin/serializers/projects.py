# -*- coding: utf-8 -*-

from flask_restplus import fields
from .nested import group_nested, file_nested
from .. import api

project_post_model = api.model('Project POST model', {
    'campus': fields.String(required=True, description='Campus ID'),
    'name': fields.String(required=True, min_length=6, description='Name')
})

project_patch_model = api.model('Project PATCH model', {
    'name': fields.String(required=False, min_length=6, description='Name')
})

project_minimal_model = api.model('Project minimal model', {
    'id': fields.String(required=True, description='Project ID'),
    'name': fields.String(required=True, description='Name')
})

project_model = api.inherit('Project model', project_minimal_model, {
    'groups': fields.List(fields.Nested(group_nested), required=True, description='Groups list'),
    'files': fields.List(fields.Nested(file_nested), required=True, description='Files list')
})

project_container = api.model('Project container', {
    'projects': fields.List(fields.Nested(project_minimal_model), required=True, description='Projects list')
})
