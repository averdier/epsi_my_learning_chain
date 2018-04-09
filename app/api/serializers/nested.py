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

user_nested = api.model('User nested', {
    'id': fields.String(required=True, description='User ID'),
    'username': fields.String(required=True, description='User username')
})

