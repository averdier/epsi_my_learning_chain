# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


campus_nested = api.model('Campus nested', {
    'id': fields.String(required=True, description='Campus ID'),
    'name': fields.String(required=True, description='Campus name')
})

project_nested = api.model('Project nested', {
    'id': fields.String(required=True, description='Project ID'),
    'name': fields.String(required=True, description='Project name')
})


student_nested = api.model('Student nested', {
    'id': fields.String(required=True, description='Student ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='First name'),
    'img_uri': fields.String(required=True, description='Img uri')
})

facilitator_nested = api.inherit('Facilitator model', student_nested, {})
