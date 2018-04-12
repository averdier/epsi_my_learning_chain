# -*- coding: utf-8 -*-

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.groups import group_container, group_model
from ..parsers import upload_parser
from app.models import Group, Project

ns = Namespace('groups', description='Groups related operations')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API Groups endpoints
#
# ================================================================================================


@ns.route('/')
class GroupCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(group_container)
    def get(self):
        """
        Return Groups
        """
        if 'campus' not in dir(g.client):
            abort(400, error='You must have campus')

        prjs = Project.objects(campus=g.client.campus)
        return {'groups': [gr for gr in Group.objects(project__in=prjs)]}


@ns.route('/<id>')
@ns.response(404, 'Group not found')
class GroupItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(group_model)
    def get(self, id):
        """
        Return Group
        """
        if 'campus' not in dir(g.client):
            abort(400, error='You must have campus')

        gr = Group.objects.get_or_404(id=id)

        if gr.project.campus != g.client.campus:
            abort(400, error='Not authorized')

        return gr


@ns.route('/<id>/upload')
class GroupItemUploader(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(group_model)
    @ns.expect(upload_parser)
    def post(self, id):
        """
        Add file
        """
        gr = Group.objects.get_or_404(id=id)

        if 'campus' not in dir(g.client):
            abort(400, error='You must have campus')


