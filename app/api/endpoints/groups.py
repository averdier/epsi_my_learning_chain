# -*- coding: utf-8 -*-

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.groups import group_resource_model, group_container, group_post_model
from app.models import Group, Project, User

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
        prjs = Project.objects(campus=g.client.campus)
        return {'groups': [gr for gr in Group.objects(project__in=prjs)]}

    @ns.marshal_with(group_resource_model)
    @ns.expect(group_post_model)
    def post(self):
        """
        Add Group
        """
        data = request.json

        p = Project.objects.get_or_404(id=data['project'])

        if p.campus != g.client.campus:
            abort(400, error='Not authorized')

        if Group.objects(project=p, name=data['name']).count() > 0:
            abort(400, error='Group name already exist')

        gr = Group(
            project=p,
            name=data['name'],
            seed=''
        )

        for u_id in data.get('users', []):
            u = User.objects.get_or_404(id=u_id)

            if u.campus != g.client.campus:
                abort(400, error='Not authorized')

            gr.users.append(u)

        gr.save()

        return gr


@ns.route('/<id>')
@ns.response(404, 'Group not found')
class GroupItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(group_resource_model)
    def get(self, id):
        """
        Return Group
        """
        gr = Group.objects.get_or_404(id=id)

        if gr.project.campus != g.client.campus:
            abort(400, error='Not authorized')

        return gr

    @ns.response(204, 'Group successfully deleted.')
    def delete(self, id):
        """
        Delete Group
        """
        gr = Group.objects.get_or_404(id=id)

        if gr.project.campus != g.client.campus:
            abort(400, error='Not authorized')

        gr.delete()

        return 'Group successfully deleted', 204
