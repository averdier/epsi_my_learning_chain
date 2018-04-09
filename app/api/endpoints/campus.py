# -*- coding: utf-8 -*-

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.campus import campus_resource, campus_container, campus_post_model, campus_put_model
from app.models import Campus


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

    @ns.marshal_with(campus_resource)
    @ns.expect(campus_post_model)
    def post(self):
        """
        Add campus
        """
        data = request.json

        if Campus.objects(name=data['name']).count() > 0:
            abort(400, error='Campus name already exist')

        c = Campus(
            name=data['name']
        )
        c.save()

        return c


@ns.route('/<id>')
@ns.response(404, 'Campus not found')
class CampusItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(campus_resource)
    def get(self, id):
        """
        Return Campus
        """
        c = Campus.objects.get_or_404(id=id)

        return c

    @ns.response(204, 'Campus successfully updated')
    @ns.expect(campus_put_model)
    def put(self, id):
        """
        Update Campus
        """
        data = request.json

        c = Campus.objects.get_or_404(id=id)
        if c != g.client.campus:
            abort(400, error='Not authorized')

        cs = Campus.objects(name=data['name']).first()

        if cs is not None and cs.id != c:
            abort(400, error='Campus name already exist')

        c.name = data['name']
        c.save()

        return 'Campus successfully updated', 204

    @ns.response(204, 'Campus successfully deleted')
    def delete(self, id):
        """
        Delete campus
        """
        c = Campus.objects.get_or_404(id=id)

        if c != g.client.campus:
            abort(400, error='Not authorized')

        c.delete()

        return 'Campus successfully deleted', 204
