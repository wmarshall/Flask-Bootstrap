# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template, request

from .assets import webpack
from .admin import Admin
from .database import db
from .auth import login_manager
from . import views
from .auth import views as auth_views
from .utils import make_json_response, JSONEncoder
from .tasks import celery

from .settings import ProdConfig

def create_app(config_object=ProdConfig):
  """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

  :param config_object: The configuration object to use.
  """
  app = Flask(__name__)
  app.config.from_object(config_object)
  app.json_encoder = JSONEncoder
  register_extensions(app)
  register_blueprints(app)
  register_errorhandlers(app)

  if app.config['ADMIN_ENABLED']:
    register_admin_interface(app)

  return app

def register_extensions(app):
  """
  Call .init_app() on known extensions
  """
  webpack.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)
  celery.init_app(app)

def register_admin_interface(app):
  """
  Call .init_app() on admin
  """
  app.admin = Admin()
  app.admin.init_app(app)

def register_blueprints(app):
  """
  Register known blueprints
  """
  app.register_blueprint(views.blueprint)
  app.register_blueprint(auth_views.blueprint)

def register_errorhandlers(app):
  """
  Register error handlers for common errors to show nice landing pages
  """
  def render_error(error):
    """render the appropriate template if possible"""
    # If a HTTPException, pull the `code` attribute; default to 500
    error_code = getattr(error, 'code', 500)
    if request.is_xhr or request.method == "POST":
      return make_json_response(code=error_code)
    else:
      return render_template("{0}.html".format(error_code)), error_code
  for errcode in [400, 403, 404, 500]:
    app.errorhandler(errcode)(render_error)
