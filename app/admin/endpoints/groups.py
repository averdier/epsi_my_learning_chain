# -*- coding: utf-8 -*-

from flask import request
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.groups import group_container, group_post_model, group_model, group_patch_model, group_full_model
from app.models import Project, Group
from utils.iota import generate_seed

ns = Namespace('groups', description='Groups related operation')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API groups endpoints
#
# ================================================================================================


@ns.route('/')
class GroupCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(group_container)
    def get(self):
        """
        Return groups
        """
        return {'groups': [gr for gr in Group.objects]}

    @ns.marshal_with(group_full_model)
    @ns.expect(group_post_model)
    def post(self):
        """
        Add group
        """
        data = request.json

        p = Project.objects.get_or_404(id=data['project'])
        if Group.objects(project=p, name=data['name']).count() > 0:
            abort(400, error='Name already exist')

        gr = Group(
            project=p,
            name=data['name'],
            seed=generate_seed()
        )

        gr.get_transfers()
        gr.save()

        return gr


@ns.route('/<id>')
class GroupItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(group_model)
    def get(self, id):
        """
        Return group
        """
        gr = Group.objects.get_or_404(id=id)

        return gr

    @ns.response(204, 'Group successfully patched')
    @ns.expect(group_patch_model)
    def patch(self, id):
        """
        Patch group
        """
        data = request.json
        if len(data) == 0:
            abort(400, error='No data')

        gr = Group.objects.get_or_404(id=id)

        gs = Group.objects(project=gr.project, name=data['name']).first()

        if gs is not None and gs.id != gr.id:
            abort(400, error='Name already exist')

        gr.name = data['name']
        gr.save()

        return 'Group successfully patched', 204

    @ns.response(204, 'Group successfully deleted')
    def delete(self, id):
        """
        Delete group
        """
        gr = Group.objects.get_or_404(id=id)

        gr.delete()

        return 'Group successfully deleted', 204


@ns.route('/<id>/details')
@ns.response(404, 'Group not found')
class GroupItemDetails(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(group_full_model)
    def get(self, id):
        """
        Return Group
        """
        gr = Group.objects.get_or_404(id=id)

        return gr