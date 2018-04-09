# -*- coding: utf-8 -*-

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.users import user_resource, user_full_resource, user_container, user_post_model
from ..parsers import user_parser
from app.models import User, Campus


ns = Namespace('users', description='Users related operations')

# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API users endpoints
#
# ================================================================================================


@ns.route('/')
class UserCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_container)
    def get(self):
        """
        Return users
        """
        args = user_parser.parse_args()
        result = {'users': []}
        if args.get('type'):
            result['users'] = [u for u in User.objects(type=args['type'])]
        else:
            result['users'] = [u for u in User.objects]

        return result

    @ns.marshal_with(user_resource)
    @ns.expect(user_post_model)
    def post(self):
        """
        Add user
        """
        data = request.json

        if data['type'] not in ['admin', 'etu', 'int']:
            abort(400, error='Unknown user type.')

        if User.objects(username=data['username']).count():
            abort(400, error='Username already exist.')

        u = User(
            campus=g.client.campus,
            type=data['type'],
            username=data['username'],
            img_uri=data.get('img_uri')
        )
        u.secret = data['secret']

        u.save()

        return u


@ns.route('/<id>')
@ns.response(404, 'User not found')
class UserItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_resource)
    def get(self, id):
        """
        Return user
        """
        u = User.objects.get_or_404(id=id)

        return u

    @ns.response(204, 'Client successfully updated.')
    def patch(self, id):
        """
        Update client
        """
        data = request.json

        u = User.objects.get_or_404(id=id)
        if u.campus != g.client.campus:
            abort(400, error='Not authorized')

        if len(data) == 0:
            abort(400, error='No data')

        if data.get('img_uri'):
            u.img_uri = data['img_uri']

        if data.get('secret'):
            u.secret = data['secret']

        u.save()

        return 'Client successfully updated.', 204

    @ns.response(204, 'Client successfully deleted.')
    def delete(self, id):
        """
        Delete user
        """
        u = User.objects.get_or_404(id=id)

        if u.campus != g.client.campus:
            abort(400, error='Not authorized')

        u.delete()

        return 'User successfully deleted.', 204


@ns.route('/<id>/full')
@ns.response(404, 'User not found')
class UserItemFull(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_full_resource)
    def get(self, id):
        """
        Return user
        """
        if g.client.type != 'admin':
            abort(400, error='Not authorized')

        u = User.objects.get_or_404(id=id)

        return u
