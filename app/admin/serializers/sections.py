# -*- coding: utf-8 -*-

from flask_restplus import fields
from .nested import campus_nested, api


section_post_model = api.model('Section POST model', {
    'campus': fields.String(required=True, description='Campus ID'),
    'year': fields.Integer(required=True, min=2017, description='Year'),
    'name': fields.String(required=True, min_length=4, description='Name')
})

section_minimal_model = api.model('Section minimal model', {
    'id': fields.String(required=True, description='Section ID'),
    'campus_id': fields.String(required=True, description='Campus ID', attribute=lambda s: s.campus.id),
    'year': fields.Integer(required=True, description='Year'),
    'name': fields.String(required=True, description='Name')
})

section_model = api.inherit('Section model', section_minimal_model, {
    'campus': fields.Nested(campus_nested, required=True, description='Campus')
})

section_container = api.model('Section container', {
    'sections': fields.List(fields.Nested(section_minimal_model), required=True, description='Sections list')
})