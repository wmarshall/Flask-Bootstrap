"""
Application.__init__.py
A skeleton for a modern webapp
"""
from . import (admin, app, assets, auth, database, models,
               settings, views, tasks, utils)

from .models import public_models, public_tables

application = app.create_app(settings.get_config_for_current_environment())
db = database.db
celery = tasks.celery
