# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


campus_nested = api.model('Campus nested', {
    'id': fields.String(required=True, description='Campus ID'),
    'name': fields.String(required=True, description='Campus name')
})

student_nested = api.model('Student nested', {
    'id': fields.String(required=True, description='Student ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='First name'),
    'img_uri': fields.String(required=True, description='Img uri')
})

group_nested = api.model('Group nested', {
    'id': fields.String(required=True, description='Group ID'),
    'name': fields.String(required=True, description='Name'),
    'students_count': fields.Integer(required=True, description='User count', attribute=lambda p: len(p.students))
})
