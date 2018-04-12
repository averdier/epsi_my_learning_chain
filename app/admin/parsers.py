# -*- coding: utf-8 -*-

from werkzeug.datastructures import FileStorage
from . import api


upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)