# -*- coding: utf-8 -*-

from flask import request
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.sections import section_post_model, section_container, section_model
from app.models import Section, Campus


ns = Namespace('sections', description='Sections related operation')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API sections endpoints
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
        return {'sections': [s for s in Section.objects]}

    @ns.marshal_with(section_model)
    @ns.expect(section_post_model)
    def post(self):
        """
        Add Section
        """
        data = request.json
        c = Campus.objects.get_or_404(id=data['campus'])

        if Section.objects(name=data['name'], campus=c).count() > 0:
            abort(400, error='Name already exist')

        s = Section(
            campus=c,
            year=data['year'],
            name=data['name']
        )

        s.save()

        return s

@ns.route('/<id>')
@ns.response(404, 'Section not found')
class SectionItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(section_model)
    def get(self, id):
        """
        Return Section
        """
        s = Section.objects.get_or_404(id=id)

        return s

    @ns.response(204, 'Section successfully deleted')
    def delete(self, id):
        """
        Delete Section
        """
        s = Section.objects.get_or_404(id=id)

        s.delete()

        return 'Section successfully deleted', 204