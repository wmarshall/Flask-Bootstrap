# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related
utilities.
"""
from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from flask import request, flash, abort
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property

from .utils import make_json_response

db = SQLAlchemy()

class CRUDMixin():
  """
  Mixin that adds convenience methods for CRUD (create, read, update, delete)
  operations.
  """
  @classmethod
  def get_or_create(cls, **kwargs):
    """
    Provides terribad upsertish behavior.
    Could be made aware of postgres On Confict for faster operation
    returns a tuple (obj, created), where created is True if the object is new
    """
    if len(kwargs) == 0:
      raise ValueError("must specify some keys.")
    try:
      return (cls.query.filter_by(**kwargs).one(), False)
    except (NoResultFound, MultipleResultsFound):
      try:
        obj = cls.create(**kwargs)
        return (obj, True)
      except IntegrityError:
        #someone created before us
        return (cls.query.filter_by(**kwargs).get(), False)

  @classmethod
  def create(cls, *, commit=True, **kwargs):
    """Create a new record and save it the database."""
    instance = cls(**kwargs)
    return instance.save(commit=commit)

  def update(self, commit=True, **kwargs):
    """Update specific fields of a record. Chainable"""
    for attr, value in kwargs:
      setattr(self, attr, value)
    return self.save(commit=commit)

  def save(self, commit=True):
    """Save the record. Chainable"""
    db.session.add(self)
    if commit:
      self.commit()
    return self

  def delete(self, commit=True):
    """Remove the record from the database."""
    db.session.delete(self)
    if commit:
      self.commit()

  @staticmethod
  def commit():
    """Do a commit."""
    db.session.commit()


class RESTMixin(CRUDMixin):
  """
  Adds rest views to the model
  """
  BASE_URL = "/rest"
  METHODS = ["GET", "PUT", "POST", "DELETE"]

  def __cols__(cls):
    return tuple()

  def __pkey__(cls):
    return tuple()

  def __serialize__(self):
    return {col: getattr(self, col) for col in self.__cols__()}

  def __serialize_pkey__(self):
    return {col: getattr(self, col) for col in self.__pkey__()}

  def __str__(self):
    return "{name}:{pkey}".format(name=type(self), pkey=self.__serialize_pkey__())

  def __repr__(self):
    return "{name}:{keys}".format(name=type(self).__name__, keys=self.__serialize__())

  @classmethod
  def view_path(cls):
    """ The path at which the view should present itself """
    return cls.BASE_URL + "/" + cls.__tablename__ + "/"

  @classmethod
  def register_rest_view(cls, app):
    """ makes view functions for the class """
    def rest_view_fn(key_path=None):
      """
      key_path = 'key1/val1/~fuzzykey2/fuzzyval2'
      if path == view_path/<key_path:path>:
        record = cls.get(key=key)
      else if path == view_path/:
        collection = cls.all()

      """
      filter_dict = {}
      if key_path is not None:
        keyvals = key_path.split("/")
        if len(keyvals) % 2 != 0:
          flash("Bad key path request", "warning")
          abort(400)
        keys = keyvals[0::2]
        vals = keyvals[1::2]
        filter_dict.update(dict(zip(keys, vals)))
      if request.get_json() is not None:
        filter_dict.update(request.get_json())
      filter_dict.update(request.args)

      fuzzy_dict = {}
      specific_dict = {}
      directive_dict = {}
      for key in filter_dict:
        if key.startswith("~"):
          fuzzy_dict[key[1:]] = filter_dict[key]
        elif key.startswith("!"):
          directive_dict[key[1:]] = filter_dict[key].split(",")
        else:
          specific_dict[key] = filter_dict[key]

      filter_dict = specific_dict

      if request.method == 'GET':
        if key_path is None: # List
          query = cls.query
          for attr in directive_dict.get("order", []):
            query = query.order_by(getattr(cls, attr))
          for attr in directive_dict.get("reverse", []):
            query = query.order_by(getattr(cls, attr).desc())
          if "limit" in directive_dict:
            query = query.limit(directive_dict["limit"])
          resources = query.all()
          return make_json_response(resources=[resource.__serialize_pkey__()
                                               for resource in resources]
                                   )
        else: #Retrieve one or more
          query = (cls.query
                       .filter_by(**filter_dict)
                       .filter(*[getattr(cls, attr).cast(db.Text).ilike("%{pattern}%".format(pattern=pattern)) for attr, pattern in fuzzy_dict.items()])
                      )
          for attr in directive_dict.get("order", []):
            query = query.order_by(getattr(cls, attr))
          for attr in directive_dict.get("reverse", []):
            query = query.order_by(getattr(cls, attr).desc())
          if "limit" in directive_dict:
            query = query.limit(directive_dict["limit"][-1])
          resources = query.all()
          if len(resources) == 0:
            abort(404)
          return make_json_response(resources=[resource.__serialize__()
                                               for resource in resources])
      elif request.method == 'PUT':
        data = request.get_json()
        if key_path is None: # Replace all, don't support for now
          abort(405)
        else: #Replace or create one (upsert)
          resource, created = cls.get_or_create(**filter_dict)
          resource.update(data)
          resp_code = 200 if not created else 201
          return make_json_response(code=resp_code)
      elif request.method == 'POST':
        if key_path is None: #Create and return pkey
          resource = cls.create(**filter_dict)
          return make_json_response(resource=[resource.__serialize_pkey__()])
        else: #Error
          abort(405)
      elif request.method == 'DELETE':
        if key_path is None: #Delete all, don't support for now
          abort(405)
        else: #Delete one
          resource = cls.query.filter_by(**filter_dict).first_or_404()
          resource.delete()
          return make_json_response()
    app.add_url_rule(cls.view_path(), 'rest/'+cls.__tablename__, rest_view_fn, methods=cls.METHODS)
    app.add_url_rule(cls.view_path() + "<path:key_path>",
                     'rest/'+cls.__tablename__+"/selector", rest_view_fn, methods=cls.METHODS)
    return rest_view_fn

class Model(RESTMixin, db.Model):
  """Base model class that includes REST and CRUD convenience methods."""
  __abstract__ = True

class ExpiresMixin():

  shelf_life = timedelta(days=7)
  last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  @hybrid_property
  def fresh(self):
    return self.last_updated > (datetime.utcnow() - self.shelf_life)

  @hybrid_property
  def expired(self):
    return self.last_updated < (datetime.utcnow() - self.shelf_life)

  def refresh(self):
    self.last_updated = datetime.utcnow()

def ReferenceCol(tablename, pk_name, nullable=False, **kwargs):
  """Column that adds primary key foreign key reference.

  Usage: ::

    category_id = ReferenceCol('category')
    category = relationship('Category', backref='categories')
  """
  return db.Column(
    db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
    nullable=nullable, **kwargs)

# Alias common SQLAlchemy names
Column = db.Column
Table = db.Table
relationship = relationship
MetaData = db.Model.metadata

__all__ = ["db", "Column", "Table", "Model", "MetaData", "relationship", "ReferenceCol", "ExpiresMixin"]
