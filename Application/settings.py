# -*- coding: utf-8 -*-
"""
settings.py
Declares settings for the application
"""
import os
import sys

### logging configure values ###############################################
from logging import config

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'standard': {
      'format': '%(asctime)s| %(name)s/%(process)d: '
                '%(message)s @%(funcName)s:%(lineno)d #%(levelname)s',
    }
  },
  'handlers': {
    'console': {
      'formatter': 'standard',
      'class': 'logging.StreamHandler'
    },
  },
  'root': {
    'handlers': ['console'],
    'level': 'INFO',
  },
  'loggers': {
    'Application': {
      'level': 'INFO',
    },
  }
}
config.dictConfig(LOGGING)
############################################################################x

class Config():
  """
  Default config
  """
  APP_NAME = "Application"

  APP_DIR = os.path.abspath(os.path.dirname(__file__))
  PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

  DATABASE_PROTO = "sqlite"
  DATABASE_USER = ""
  DATABASE_PASS = ""
  DATABASE_HOST = ""
  DATABASE_NAME = "spinneret"
  SQLALCHEMY_DATABASE_URI = ("{proto:s}://{user:s}:"
                             "{passwd:s}@{host:s}/"
                             "{name:s}".format(proto=DATABASE_PROTO,
                                               user=DATABASE_USER,
                                               passwd=DATABASE_PASS,
                                               host=DATABASE_HOST,
                                               name=DATABASE_NAME))

  SQLALCHEMY_TRACK_MODIFICATIONS = False


  BROKER_PROTO = "amqp://"
  BROKER_HOST = "localhost"
  BROKER_URL = BROKER_PROTO + BROKER_HOST
  CELERY_RESULT_BACKEND = "db+"+SQLALCHEMY_DATABASE_URI
  CELERY_ACCEPT_CONTENT = ["json"]
  CELERY_TASK_SERIALIZER = "json"
  CELERY_IGNORE_RESULT = False
  CELERY_RESULT_SERIALIZER = "json"
  CELERY_RESULT_PERSISTENT = False
  CELERYD_POOL_RESTARTS = True

  ADMIN_ENABLED = True

  WEBPACK_MANIFEST_PATH = os.path.join(APP_DIR, "app_src/manifest.json")
  WEBPACK_ASSETS_URL = None
  ASSETS_URL = None #Special redirect magic, see assets.py

class ProdConfig(Config):
  """Production configuration."""
  ENV = 'prod'
  DEBUG = False


class DevConfig(Config):
  """Development configuration."""
  ENV = 'dev'
  DEBUG = True

  # EXPLAIN_TEMPLATE_LOADING = True

  # Uncomment this line to debug javascript/css assets
  # ASSETS_DEBUG = True
  SECRET_KEY = "dontprodme".encode("utf-8")

  DATABASE_NAME = 'my_apps_db'
  SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DATABASE_NAME

  # Ease up on password requirements in dev to allow simple testing
  PASSWORD_REQUIRE_MIN = 4
  PASSWORD_REQUIRE_SPECIAL = False
  PASSWORD_REQUIRE_UPPER = False
  PASSWORD_REQUIRE_LOWER = False
  PASSWORD_REQUIRE_NUMBER = False

class TestConfig(Config):
  """
  Lite config for testing
  """
  TESTING = True
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite://'
  BCRYPT_LOG_ROUNDS = 1  # For faster tests
  WTF_CSRF_ENABLED = False  # Allows form testing
  ADMIN_ENABLED = False

class DockerConfig(ProdConfig):
  pass

def get_config_for_current_environment():
  """
  Checks environment variable, picks correct config
  """
  if len(sys.argv) > 1 and sys.argv[1] == 'test':
    return TestConfig
  elif os.environ.get("APP_ENV") == 'dev':
    return DevConfig
  elif os.environ.get("APP_ENV") == 'docker':
    return DockerConfig()
  else:
    # stage, demo, prod, etc. all get prod-like settings (e.g. no asset debugging)
    return ProdConfig
