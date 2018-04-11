# -*- coding: utf-8 -*-

import os
import jwt
from configobj import ConfigObj
from flask import Blueprint, current_app, g
from flask_httpauth import HTTPTokenAuth
from flask_restplus import Api
from app.models import User


conf_path = os.environ.get('APP_SETTINGS', None)
if not conf_path:
    raise Exception('Unable to find APP_SETTINGS.')

conf = ConfigObj(conf_path)
config_name = conf.get('CONFIG', 'default')


blueprint = Blueprint('admin', __name__, url_prefix='/admin')
api = Api(blueprint,
          title='My Learning Chain',
          version='0.1',
          description='Python admin learning chain backend',
          authorizations={
              'tokenKey': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization'
              }
          },
          security='tokenKey',
          doc='/' if config_name != 'production' else False
          )


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    """
    Verify authorization token
    :param token:
    :return:
    """

    try:
        response = jwt.decode(
            token,
            current_app.config['PUBLIC_KEY'],
            audience=''
        )

        u = User.objects.get(id=response['user']['id'])

        if u is None:
            return False

        else:
            g.client = u
            return True

    except Exception as ex:
        print(ex)
        return False


from .endpoints.campus import ns as campus_namespace
from .endpoints.sections import ns as sections_namespace
from .endpoints.facilitators import ns as facilitators_namespace
from .endpoints.students import ns as students_namespace
from .endpoints.projects import ns as projects_namespace
from .endpoints.groups import ns as groups_namespace
from .endpoints.facilitators import ns as facilitators_namespace

if config_name != 'production':
    from .endpoints.postman import ns as postman_namespace
    api.add_namespace(postman_namespace)

api.add_namespace(campus_namespace)
api.add_namespace(sections_namespace)
api.add_namespace(facilitators_namespace)
api.add_namespace(students_namespace)
api.add_namespace(projects_namespace)
api.add_namespace(facilitators_namespace)
api.add_namespace(groups_namespace)

