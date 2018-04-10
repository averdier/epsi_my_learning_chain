# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api

iota_address_model = api.model('IOTA Address model', {
    'address': fields.String(required=True, description='Address')
})

iota_account_model = api.model('IOTA Account model', {
    'id': fields.String(required=True, description='Account ID'),
    'seed': fields.String(required=True, description='Account seed'),
    'deposit_address': fields.Nested(iota_address_model, required=True, description='Account deposit address')
})
