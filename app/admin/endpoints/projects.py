# -*- coding: utf-8 -*-

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.projects import project_model, project_container, project_post_model, project_patch_model
from app.models import Project, Campus

ns = Namespace('projects', description='Projects related operations')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API Projects endpoints
#
# ================================================================================================


@ns.route('/')
class ProjectCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(project_container)
    def get(self):
        """
        Return Projects
        """
        return {'projects': [p for p in Project.objects]}

    @ns.marshal_with(project_model)
    @ns.expect(project_post_model)
    def post(self):
        """
        Add project
        """
        data = request.json

        c = Campus.objects.get_or_404(id=data['campus'])

        if Project.objects(campus=c, name=data['name']).count() > 0:
            abort(400, error='Name already exist')

        p = Project(
            campus=c,
            name=data['name']
        )

        p.save()

        return p


@ns.route('/<id>')
@ns.response(404, 'Project not found')
class ProjectItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(project_model)
    def get(self, id):
        """
        Return Project
        """
        p = Project.objects.get_or_404(id=id)

        return p

    @ns.response(204, 'Project successfully patched')
    @ns.expect(project_patch_model)
    def patch(self, id):
        """
        Patch Project
        """
        data = request.json
        if len(data) == 0:
            abort(400, error='No data')

        p = Project.objects.get_or_404(id=id)

        ps = Project.objects(campus=p.campus, name=data['name']).first()

        if ps is not None and ps.id != p.id:
            abort(400, error='Name already exist')

        p.name = data['name']

        p.save()

        return 'Project successfully patched', 204

    @ns.response(204, 'Project successfully deleted')
    def delete(self, id):
        """
        Delete Project
        """
        p = Project.objects.get_or_404(id=id)

        p.delete()

        return 'Project successfully deleted', 204
