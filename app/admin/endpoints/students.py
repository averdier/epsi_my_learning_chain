# -*- coding: utf-8 -*-

from flask import request
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.students import student_container, student_model, student_post_model, student_patch_model
from app.models import User, Student, Campus, Section


ns = Namespace('students', description='Students related operation')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API Students endpoints
#
# ================================================================================================

@ns.route('/')
class StudentCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(student_container)
    def get(self):
        """
        Return students
        """
        return {'students': [s for s in Student.objects]}

    @ns.marshal_with(student_model)
    def post(self):
        """
        Add student
        """
        data = request.json

        c = Campus.objects.get_or_404(data['campus'])
        sc = Section.objects.get_or_404(data['section'])

        if User.objects(username=data['username']).count() > 0:
            abort(400, error='Username already exist')

        if User.objects(email=data['email']).count() > 0:
            abort(400, error='Email already exist')

        s = Student()
        s.campus = c
        s.section = sc
        s.first_name = data['first_name']
        s.last_name = data['last_name']
        s.email = data['email']
        s.username = data['username']
        s.img_uri = data.get('img_uri')
        s.scopes = data['scopes']

        s.secret = data['secret']

        return s


@ns.route('/<id>')
@ns.response(404, 'Student not found')
class StudentItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(student_model)
    def get(self, id):
        """
        Return student
        """
        s = Student.object.get_or_404(id=id)

        return s

    @ns.response(204, 'Student successfully patched')
    def patch(self, id):
        """
        Patch student
        """
        s = Student.object.get_or_404(id=id)
        data = request.json

        if len(data) == 0:
            abort(400, error='No data')

        if data['first_name']:
            s.first_name = data['first_name']

        if data['last_name']:
            s.last_name = data['last_name']

        if data['email']:
            us = User.objects(email=data['email']).first()
            if us is not None and us.id != id:
                abort(400, error='Email already exist')

            s.email = data['email']

        if data['img_uri']:
            s.img_uri = data['img_uri']

        if data['secret']:
            s.secret = data['secret']

        if data['scopes']:
            s.scopes = data['scopes']

        s.save()

        return 'Student successfully patched', 204

    @ns.response(204, 'Student successfully deleted')
    def delete(self, id ):
        """
        Delete Student
        """
        s = Student.object.get_or_404(id=id)

        s.delete()

        return 'Student successfully deleted'
