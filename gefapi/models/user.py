"""USER MODEL"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import uuid

from werkzeug.security import generate_password_hash, \
     check_password_hash

from gefapi.models import GUID
from gefapi import db
db.GUID = GUID


class User(db.Model):
    """User Model"""
    id = db.Column(db.GUID(), default=uuid.uuid4, primary_key=True, autoincrement=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    role = db.Column(db.String(10))
    scripts = db.relationship('Script', backref='user', lazy='dynamic')
    executions = db.relationship('Execution', backref='user', lazy='dynamic')

    def __init__(self, email, password, role='USER'):
        self.email = email
        self.password = self.set_password(password=password)
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self, include=None):
        """Return object data in easily serializeable format"""
        include = include if include else []
        user = {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at,
            'role': self.role,
        }
        if 'scripts' in include:
            user['scripts'] = self.serialize_scripts
        return user

    @property
    def serialize_scripts(self):
        """Serialize Scripts"""
        return [item.serialize() for item in self.scripts]

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
