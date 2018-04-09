# -*- coding: utf-8 -*-

from flask_restplus import fields
from .nested import project_nested, campus_nested, user_nested, api

group_post_model = api.model('Group POST model', {
    'project': fields.String(required=True, description='Project ID'),
    'name': fields.String(required=True, min_length=6, description='Group name'),
    'users': fields.List(fields.String(), required=False, description='Users ID list')
})

group_resource_model = api.model('Group resource model', {
    'id': fields.String(required=True, description='Group ID'),
    'name': fields.String(required=True, description='Group name'),
    'project': fields.Nested(project_nested, required=True, description='Group project'),
    'campus': fields.Nested(campus_nested, attribute=lambda g: g.project.campus, description='Group campus'),
    'users': fields.List(fields.Nested(user_nested), required=True, description='Group users')
})

group_container = api.model('Group container', {
    'groups': fields.List(fields.Nested(group_resource_model), required=True, description='Groups list')
})

