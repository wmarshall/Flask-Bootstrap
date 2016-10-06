# -*- coding: utf-8 -*-
"""
models.py
"""
import datetime as dt

from flask_login import UserMixin, make_secure_token
from . import crypto
from ..database import (Model, Column, db, ReferenceCol,
                        relationship)


class Role(Model):
  """
  A user's Role, allows them to perform certain actions
  """
  __tablename__ = 'roles'

  name = Column(db.String(80), primary_key=True)
  user_id = ReferenceCol('users', pk_name='username', primary_key=True)
  user = relationship('User', backref='roles')

  def __str__(self):
    return 'Role({name}, {user})'.format(name=self.name, user=self.user)

  def __cols__(self):
    return ("name", "user_id", "user")

  def __pkey__(self):
    return ("name", "user_id")


class User(UserMixin, Model):
  """
  A user, capable of logging in and performing actions
  """
  __tablename__ = 'users'

  username = Column(db.String(80), primary_key=True)
  password = Column(db.LargeBinary(256), nullable=True)
  salt = Column(db.LargeBinary(256), nullable=True)
  full_name = Column(db.String(80), nullable=True)
  active = Column(db.Boolean(), default=False)
  is_admin = Column(db.Boolean(), default=False)
  created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

  def __init__(self, username=None, password=None, **kwargs):
    db.Model.__init__(self, username=username, **kwargs)
    if password:
      self.set_password(password)
    else:
      self.password = None

  def set_password(self, password):
    """Hashes and stores plaintext password"""
    self.salt = crypto.generate_random_salt()
    self.password = crypto.generate_password_hash(password, self.salt)

  def check_password(self, value):
    """Constant time check of password"""
    return crypto.check_password_hash(value, self.password, self.salt)

  def has_role(self, role, ignore_super=False):
    """
    Checks if user has a given role. Admins are assumed to have all roles.

    If *ignore_super* is not set to true,
    """
    if not ignore_super and self.is_admin:
      return True
    if role == "admin":
      return self.is_admin
    return any(str(role) == str(r) for r in self.roles)

  def get_id(self):
    return self.username

  def get_auth_token(self):
    return make_secure_token(self.username, self.salt, self.password)

  def __serialize__(self):
    """
    represents user as json object, omitting sensitive columns
    """
    return {
      'username': self.username,
      'full_name': self.full_name,
      'active': self.active
    }

  def __serialize_pkey__(self):
    return {
      "username": self.username
    }

  def __repr__(self):
    return '{username}'.format(username=self.username)

AdminModels = [Role, User]
