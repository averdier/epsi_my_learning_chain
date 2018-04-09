# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


section_post_model = api.model('Section POST model', {
    'year': fields.Integer(required=True, min=2018, description='Year of section'),
    'name': fields.String(required=True, min_length=3, description='Section name')
})

section_resource_model = api.model('Section resource model', {
    'id': fields.String(required=True, description='Section ID'),
    'year': fields.Integer(required=True, description='Year of section'),
    'name': fields.String(required=True, description='Section name')
})

section_container = api.model('Section container', {
    'sections': fields.List(fields.Nested(section_resource_model), required=True, description='Sections list')
})