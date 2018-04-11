# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


claim_post_model = api.model('Claim POST model', {
    'offer': fields.String(required=True)
})