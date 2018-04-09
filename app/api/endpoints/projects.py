# -*- coding: utf-8 -*-

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.projects import project_resource_model, project_container, project_post_model
from app.models import Project


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
        return {'projects': [p for p in Project.objects(campus=g.client.campus)]}

    @ns.marshal_with(project_resource_model)
    @ns.expect(project_post_model)
    def post(self):
        """
        Add project
        """
        data = request.json

        if Project.objects(campus=g.client.campus, name=data['name']).count() > 0:
            abort(400, error='Project name already exist')

        p = Project(
            campus=g.client.campus,
            name=data['name']
        )

        p.save()

        return p


@ns.route('/<id>')
@ns.response(404, 'Project not found')
class ProjectItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(project_resource_model)
    def get(self, id):
        """
        Return Project
        """
        p = Project.objects.get_or_404(id=id)

        if p.campus != g.client.campus:
            abort(400, error='Not authorized')

        return p

    @ns.response(204, 'Project successfully deleted.')
    def delete(self, id):
        """
        Delete Project
        """
        p = Project.objects.get_or_404(id=id)

        if p.campus != g.client.campus:
            abort(400, error='Not authorized')

        p.delete()

        return 'Project successfully deleted', 204
