# -*- coding: utf-8 -*-

from flask import request
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.campus import campus_post_model, campus_container, campus_model, campus_full_model, \
    campus_patch_model
from app.models import Campus
from utils.iota import generate_seed

ns = Namespace('campus', description='Campus related operation')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API campus endpoints
#
# ================================================================================================


@ns.route('/')
class CampusCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(campus_container)
    def get(self):
        """
        Return Campus
        """
        return {'campus': [c for c in Campus.objects]}

    @ns.marshal_with(campus_full_model)
    @ns.expect(campus_post_model)
    def post(self):
        """
        Add campus
        """
        data = request.json

        if Campus.objects(name=data['name']).count() > 0:
            abort(400, error='Campus name already exist')

        c = Campus(
            name=data['name'],
            seed=generate_seed(),
            description=data.get('description', '')
        )
        d = c.deposit_address
        c.save()

        return c


@ns.route('/<id>')
@ns.response(404, 'Campus not found')
class CampusItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(campus_model)
    def get(self, id):
        """
        Return Campus
        """
        c = Campus.objects.get_or_404(id=id)

        return c

    @ns.response(204, 'Campus successfully patched')
    @ns.expect(campus_patch_model)
    def patch(self, id):
        """
        Patch Campus
        """
        c = Campus.objects.get_or_404(id=id)
        data = request.json

        if len(data) == 0:
            abort(400, error='No data')

        if data['name']:
            cs = Campus.objects(name=data['name']).first()
            if cs is not None and cs.id != id:
                abort(400, error='Name already exist')

            c.name = data['name']

        if data['description']:
            c.description = data['description']

        c.save()

        return 'Campus successfully patched', 204

    @ns.response(204, 'Campus successfully deleted')
    def delete(self, id):
        """
        Delete campus
        """
        c = Campus.objects.get_or_404(id=id)

        c.delete()

        return 'Campus successfully deleted', 204


@ns.route('/<id>/details')
@ns.response(404, 'Campus not found')
class CampusItemDetails(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(campus_full_model)
    def get(self, id):
        """
        Return Campus
        """
        c = Campus.objects.get_or_404(id=id)

        return c
