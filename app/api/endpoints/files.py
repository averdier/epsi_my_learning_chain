# -*- coding: utf-8 -*-

from flask import request, send_file
from flask_restplus import Namespace, Resource, abort
from .. import auth
from app.models import File, Campus, Project


ns = Namespace('files', description='Files related operation')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API files endpoints
#
# ================================================================================================


@ns.route('/<id>')
@ns.response(404, 'File not found')
class FileItem(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        """
        Return file
        """
        f = File.objects.get_or_404(id=id)

        return send_file(f.path)