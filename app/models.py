# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from datetime import datetime


class Campus(db.Document):
    """
    Campus model
    """
    created_at = db.DateTimeField(default=datetime.now())
    name = db.StringField(required=True, unique=True)


class User(db.Document):
    """
    User model
    """
    created_at = db.DateTimeField(default=datetime.now())
    campus = db.ReferenceField(Campus, required=True)
    type = db.StringField(required=True)
    username = db.StringField(required=True, unique=True)
    img_uri = db.StringField()
    secret_hash = db.StringField()
    scopes = db.ListField(db.StringField)

    @property
    def secret(self):
        return self.secret_hash

    @secret.setter
    def secret(self, pwd):
        self.secret_hash = generate_password_hash(pwd)

    def check_secret(self, pwd):
        if not self.secret_hash:
            return False
        return check_password_hash(self.secret_hash, pwd)

    def to_dict(self):
        return {
            'created_at': self.created_at,
            'campus': self.campus,
            'type': self.type,
            'username': self.username,
            'img_uri': self.img_uri,
            'scopes': self.scopes
        }
