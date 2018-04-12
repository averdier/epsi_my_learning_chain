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

claim_nested = api.model('Claim nested', {
    'id': fields.String(required=True, description='Claim ID'),
    'offer_id': fields.String(required=True, description='Offer ID', attribute=lambda c: c.offer.id),
    'status': fields.String(required=True, description='Status')
})

file_nested = api.model('File nested', {
    'id': fields.String(required=True, description='File ID'),
    'name': fields.String(required=True, description='Filename'),
    'extension': fields.String(required=True, description='Extension')
})

project_nested = api.model('Project nested', {
    'id': fields.String(required=True, description='Project ID'),
    'name': fields.String(required=True, description='Name')
})
