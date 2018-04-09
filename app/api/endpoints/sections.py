# -*- coding: utf-8 -*-

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.sections import section_resource_model, section_container, section_post_model
from app.models import Section


ns = Namespace('sections', description='Sections related operations')

# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API Sections endpoints
#
# ================================================================================================


@ns.route('/')
class SectionCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(section_container)
    def get(self):
        """
        Return Sections
        """
        return {'sections': [s for s in Section.objects(campus=g.client.campus)]}

    @ns.marshal_with(section_resource_model)
    @ns.expect(section_post_model)
    def post(self):
        """
        Add section
        """
        data = request.json

        if Section.objects(campus=g.client.campus, name=data['name']).count() > 0:
            abort(400, error='Section name already exist')

        s = Section(
            campus=g.client.campus,
            year=data['year'],
            name=data['name']
        )
        s.save()

        return s


@ns.route('/<id>')
@ns.response(404, 'Section not found')
class SectionItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(section_resource_model)
    def get(self, id):
        """
        Return section
        """
        s = Section.objects.get_or_404(id=id)

        if s.campus != g.client.campus:
            abort(400, error='Not authorized')

        return s

    @ns.response(204, 'Section successfully deleted')
    def delete(self, id):
        """
        Delete section
        """
        s = Section.objects.get_or_404(id=id)

        if s.campus != g.client.campus:
            abort(400, error='Not authorized')

        s.delete()

        return 'Section successfully deleted', 204
