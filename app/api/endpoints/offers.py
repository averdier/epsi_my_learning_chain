# -*- coding: utf-8 -*-

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.offers import offer_container, offer_post_model, offer_patch_model, offer_model
from app.models import Offer

ns = Namespace('offers', description='Offers related operations')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API Offers endpoints
#
# ================================================================================================


@ns.route('/')
class OfferCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(offer_container)
    def get(self):
        """
        Return Offers
        """
        return {'offers': [o for o in Offer.objects]}

    @ns.marshal_with(offer_model)
    @ns.expect(offer_post_model)
    def post(self):
        """
        Add Offer
        """
        data = request.json

        if g.client.type != 'facilitator':
            abort(400, error='You must be facilitator')

        if Offer.objects(name=data['name']).count() > 0:
            abort(400, error='Name already exist')

        o = Offer(
            facilitator=g.client.type,
            name=data['name'],
            tags=data.get('tags'),
            price=data['price'],
            description=data.get('description')
        )

        o.save()

        return o


@ns.route('/<id>')
@ns.response(404, 'Offer not found')
class OfferItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(offer_model)
    def get(self, id):
        """
        Return Offer
        """
        o = Offer.objects.get_or_404(id=id)

        return o

    @ns.response(204, 'Offer successfully patched')
    @ns.expect(offer_patch_model)
    def patch(self, id):
        """
        Patch Offer
        """
        data = request.json
        o = Offer.objects.get_or_404(id=id)

        if o.facilitator.id != g.client.id:
            abort(400, error='Not authorized')

        if len(data) == 0:
            abort(400, error='No data')

        if data.get('name'):
            os = Offer.objects(name=data['name']).first()

            if os is not None and os.id != o.id:
                abort(400, error='Name already exist')

            o.name = data['name']

        if data.get('tags'):
            o.tags = data['tags']

        if data.get('price'):
            o.price = data['price']

        if data.get('description'):
            o.description = data['description']

        o.save()

        return 'Offer successfully patched', 204

    @ns.response(204, 'Offer successfully deleted')
    def delete(self, id):
        """
        Delete Offer
        """
        o = Offer.objects.get_or_404(id=id)

        if o.facilitator.id != g.client.id:
            abort(400, error='Not authorized')

        o.delete()

        return 'Offer successfully deleted', 204


@ns.route('/<id>/claims')
@ns.response(404, 'Offer not found')
class OfferClaim(Resource):
    decorators = [auth.login_required]


