# -*- coding: utf-8 -*-

from flask import request, current_app
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.students import student_container, student_model, student_post_model, student_patch_model
from app.models import User, Student, Campus, Section
from utils.email import send_mail_with_service


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
    @ns.expect(student_post_model)
    def post(self):
        """
        Add student
        """
        data = request.json

        c = Campus.objects.get_or_404(id=data['campus'])
        sc = Section.objects.get_or_404(id=data['section'])

        if User.objects(username=data['username']).count() > 0:
            abort(400, error='Username already exist')

        if User.objects(email=data['email']).count() > 0:
            abort(400, error='Email already exist')

        s = Student(
            campus=c,
            section=sc,
            type='student',
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            img_uri=data.get('img_uri'),
            scopes=data.get('scopes', [''])
        )

        s.secret = data['secret']

        s.save()

        try:
            send_mail_with_service({
                'server': current_app.config['EMAIL_HOST'],
                'recipients': [s.email],
                'subject': 'Bienvenue',
                'body': "Bienvenue à l'EPSI {0}, vous êtes un étudiant".format(c.name)
            })
        except Exception as ex:
            current_app.logger.error(ex)

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
        s = Student.objects.get_or_404(id=id)

        return s

    @ns.response(204, 'Student successfully patched')
    @ns.expect(student_patch_model)
    def patch(self, id):
        """
        Patch student
        """
        s = Student.objects.get_or_404(id=id)
        data = request.json

        if len(data) == 0:
            abort(400, error='No data')

        if data.get('first_name'):
            s.first_name = data['first_name']

        if data.get('last_name'):
            s.last_name = data['last_name']

        if data.get('email'):
            us = Student.objects(email=data['email']).first()
            if us is not None and us.id != s.id:
                abort(400, error='Email already exist')

            s.email = data['email']

        if data.get('img_uri'):
            s.img_uri = data['img_uri']

        if data.get('secret'):
            s.secret = data['secret']

        if data.get('scopes'):
            s.scopes = data['scopes']

        s.save()

        return 'Student successfully patched', 204

    @ns.response(204, 'Student successfully deleted')
    def delete(self, id ):
        """
        Delete Student
        """
        s = Student.objects.get_or_404(id=id)

        s.delete()

        return 'Student successfully deleted', 204
