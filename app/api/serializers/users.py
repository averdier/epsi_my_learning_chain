# -*- coding: utf-8 -*-

from flask_restplus import fields
from .nested import campus_nested, api


user_post_model = api.model('User POST model', {
    'type': fields.String(required=True, description='User type (admin | etu | int)'),
    'username': fields.String(required=True, min_length=4, description='User username'),
    'img_uri': fields.String(required=False, description='User img URI'),
    'secret': fields.String(required=True, min_length=8, description='User secret')
})

user_patch_model = api.model('User PATCH model', {
    'img_uri': fields.String(required=False, description='User img URI'),
    'secret': fields.String(required=False, min_length=4, description='User secret')
})

user_resource = api.model('User resource', {
    'id': fields.String(required=True, description='User ID'),
    'type': fields.String(required=True, description='User type'),
    'campus': fields.Nested(campus_nested, required=True, description='User campus'),
    'username': fields.String(required=True, description='User username')
})

user_full_resource = api.inherit('User full resource', user_resource, {
    'scopes': fields.List(fields.String(), required=True, description='User scopes')
})

user_container = api.model('User container', {
    'users': fields.List(fields.Nested(user_resource), required=True, description='User scopes')
})
