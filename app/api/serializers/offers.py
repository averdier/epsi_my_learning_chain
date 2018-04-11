# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


offer_post_model = api.model('Offer POST model', {
    'facilitator': fields.String(required=True, description='Facilitator ID'),
    'name': fields.String(required=True, min_length=4, description='Name'),
    'tags': fields.List(fields.String(), required=False, description='Tags'),
    'price': fields.Integer(required=True, min=0, description='Price'),
    'description': fields.String(required=False, description='Description')
})

offer_minimal_model = api.model('Offer minimal model', {
    'id': fields.String(required=True)
})
