# -*- coding: utf-8 -*-

from flask import request, current_app
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.facilitators import facilitator_container, facilitator_full_model, \
    facilitator_patch_model, facilitator_post_model
from app.models import Facilitator
from utils.iota import generate_seed
from utils.email import send_mail_with_service

ns = Namespace('facilitators', description='Facilitators related operation')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API facilitators endpoints
#
# ================================================================================================


@ns.route('/')
class FacilitatorCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(facilitator_container)
    def get(self):
        """
        Return Facilitators
        """

        return {'facilitators': [f for f in Facilitator.objects]}

    @ns.marshal_with(facilitator_full_model)
    @ns.expect(facilitator_post_model)
    def post(self):
        """
        Add Facilitator
        """
        data = request.json

        if Facilitator.objects(username=data['username']).count() > 0:
            abort(400, error='Username already exist')

        if Facilitator.objects(email=data['email']).count() > 0:
            abort(400, error='Email already exist')

        f = Facilitator()
        f.type = 'facilitator'
        f.first_name = data['first_name']
        f.last_name = data['last_name']
        f.email = data['email']
        f.username = data['username']
        f.img_uri = data.get('img_uri')
        f.scopes = data['scopes']
        f.seed = generate_seed()
        f.secret = data['secret']

        f.get_transfers()

        f.save()

        try:
            send_mail_with_service({
                'server': current_app.config['EMAIL_HOST'],
                'recipients': [f.email],
                'subject': 'Bienvenue',
                'body': "Bienvenue à l'EPSI, vous êtes un intervenant"
            })
        except Exception as ex:
            current_app.logger.error(ex)

        return f


@ns.route('/<id>')
@ns.response(404, 'Facilitator not found')
class FacilitatorItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(facilitator_full_model)
    def get(self, id):
        """
        Return Facilitator
        """
        f = Facilitator.objects.get_or_404(id=id)

        return f

    @ns.response(204, 'Facilitator successfully patched')
    @ns.expect(facilitator_patch_model)
    def patch(self, id):
        """
        Patch Facilitator
        """
        f = Facilitator.objects.get_or_404(id=id)
        data = request.json

        if len(data) == 0:
            abort(400, error='No data')

        if data.get('first_name'):
            f.first_name = data['first_name']

        if data.get('last_name'):
            f.last_name = data['last_name']

        if data.get('email'):
            fs = Facilitator.objects(email=data['email']).first()
            if fs is not None and fs.id != id:
                abort(400, error='Email already exist')

            f.email = data['email']

        if data.get('img_uri'):
            f.img_uri = data['img_uri']

        if data.get('secret'):
            f.secret = data['secret']

        if data.get('scopes'):
            f.scopes = data['scopes']

        f.save()

        return 'Facilitator successfully patched', 204

    @ns.response(204, 'Facilitator successfully deleted')
    def delete(self, id):
        """
        Delete Facilitator
        """
        f = Facilitator.objects.get_or_404(id=id)

        f.delete()

        return 'Facilitator successfully deleted', 204
