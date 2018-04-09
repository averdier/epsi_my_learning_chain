# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api
from .users import user_full_resource


jwks_model = api.model('jwks.json model', {
    'alg': fields.String(required=True, description='Algorithm'),
    'e': fields.String(required=True, description='?'),
    'n': fields.String(required=True, description='Public key'),
    'kty': fields.String(required=True, description='?'),
    'use': fields.String(required=True, description='?')
})

token_model = api.model('Token model', {
    'iss': fields.String(required=True, desctiption='Issuer'),
    'aud': fields.String(required=True, description='Audience'),
    'iat': fields.Integer(required=True, description='Issued at'),
    'exp': fields.Integer(required=True, description='Expiration time'),
    'user': fields.Nested(user_full_resource, required=True, description='User')
})


access_token = api.model('Access token', {
    'access_token': fields.String(required=True, description='Token')
})

verify_token_parameters = api.model('Verify token parameters', {
    'access_token': fields.String(required=True, description='Token')
})
