# -*- coding: utf-8 -*-

from . import api


user_parser = api.parser()
user_parser.add_argument('type', required=False, type=str, help="User type")


auth_parser = api.parser()
auth_parser.add_argument('username', required=True, type=str, help='Client username', location='form')
auth_parser.add_argument('secret', required=True, type=str, help='Client secret', location='form')