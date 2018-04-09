# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


campus_nested = api.model('Campus nested user', {
    'id': fields.String(required=True, description='Campus ID'),
    'name': fields.String(required=True, description='Campus name')
})