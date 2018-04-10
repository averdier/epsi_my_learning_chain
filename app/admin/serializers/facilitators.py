# -*- coding: utf-8 -*-

from flask_restplus import fields
from .iota import iota_address_model, api


facilitator_post_model = api.model('Facilitator POST model', {
    'first_name': fields.String(required=True, min_length=4, description='First name'),
    'last_name': fields.String(required=True, min_length=4, description='Last name'),
    'username': fields.String(required=True, min_length=6, description='Username'),
    'email': fields.String(required=True, description='Email address'),
    'secret': fields.String(required=True, min=6, description='Secret'),
    'img_uri': fields.String(required=False, description='Img uri')
})

facilitator_patch_model = api.model('Facilitator PATCH model', {
    'first_name': fields.String(required=False, min_length=4, description='First name'),
    'last_name': fields.String(required=False, min_length=4, description='Last name'),
    'email': fields.String(required=False, description='Email address'),
    'secret': fields.String(required=False, min=6, description='Secret'),
    'img_uri': fields.String(required=False, description='Img uri')
})

facilitator_minimal_model = api.model('Facilitator minimal model', {
    'id': fields.String(required=True, description='Facilitator ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='First name'),
    'img_uri': fields.String(required=True, description='Img uri')
})

facilitator_model = api.inherit('Facilitator model', facilitator_minimal_model, {
    'email': fields.String(required=True, description='Email')
})

facilitator_full_model = api.inherit('Facilitator full model', {
    'balance': fields.Integer(required=True, description='Facilitator balance'),
    'deposit_address': fields.Nested(iota_address_model, required=True, description='Facilitator deposit address')
})

facilitator_container = api.model('Facilitator container', {
    'facilitators': fields.List(fields.Nested(facilitator_minimal_model), required=True, description='Facilitators list')
})