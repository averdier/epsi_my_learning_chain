# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api

project_post_model = api.model('Project POST model', {
    'campus': fields.String(required=True, description='Campus ID'),
    'name': fields.String(required=True, min_length=6, description='Name')
})

project_patch_model = api.model('Project PATCH model', {
    'name': fields.String(required=False, min_length=6, description='Name')
})

project_model = api.model('Project model', {
    'id': fields.String(required=True, description='Project ID'),
    'name': fields.String(required=True, description='Name')
})

project_container = api.model('Project container', {
    'projects': fields.List(fields.Nested(project_model), required=True, description='Projects list')
})