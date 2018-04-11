# -*- coding: utf-8 -*-

from flask_restplus import fields
from .nested import student_nested, claim_nested
from .iota import iota_address_model, api


group_post_model = api.model('Group POST model', {
    'project': fields.String(required=True, description='Project ID'),
    'name': fields.String(required=True, min_length=4, description='Name')
})

group_supply_model = api.model('Group supply model', {
    'campus': fields.String(required=True, description='Campus ID'),
    'value': fields.Integer(required=True, description='Value')
})

group_patch_model = api.model('Group patch model', {
    'name': fields.String(required=False, min_length=4, description='Name')
})

group_minimal_model = api.model('Group minimal model', {
    'id': fields.String(required=True, description='Group ID'),
    'project_id': fields.String(required=True, description='Project ID', attribute=lambda p: p.project.id),
    'name': fields.String(required=True, description='Name'),
    'students_count': fields.Integer(required=True, description='User count', attribute=lambda p: len(p.students))
})

group_model = api.inherit('Group model', group_minimal_model, {
    'students': fields.List(fields.Nested(student_nested), required=True, description='Students list')
})

group_full_model = api.inherit('Group full model', group_model, {
    'claims': fields.List(fields.Nested(claim_nested), required=True, description='Claims'),
    'balance': fields.Integer(required=True, description='Group balance'),
    'deposit_address': fields.Nested(iota_address_model, required=True, description='Group deposit address')
})

group_container = api.model('Group container', {
    'groups': fields.List(fields.Nested(group_minimal_model), required=True, description='Groups list')
})