# -*- coding: utf-8 -*-

from flask_restplus import fields
from .nested import group_nested
from .facilitators import facilitator_post_model, facilitator_patch_model
from .. import api


student_post_model = api.inherit('Student POST model', facilitator_post_model, {
    'campus': fields.String(required=True, description='Campus ID'),
    'section': fields.String(required=True, description='Section ID')
})

student_patch_model = api.inherit('Student PATCH model', facilitator_patch_model, {})

student_minimal_model = api.model('Student minimal model', {
    'id': fields.String(required=True, description='Student ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='First name'),
    'img_uri': fields.String(required=True, description='Img uri')
})

student_model = api.inherit('Student model', student_minimal_model, {
    'email': fields.String(required=True, description='Email'),
    'scopes': fields.List(fields.String(), required=True, description='Scopes'),
    'groups': fields.List(fields.Nested(group_nested), required=True, description='Groups list')
})

student_container = api.model('Student container', {
    'students': fields.List(fields.Nested(student_minimal_model), required=True, description='Students list')
})
