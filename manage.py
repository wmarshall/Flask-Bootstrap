#!/usr/bin/env python3
"""
manage.py
Run the things this application needs to survive.
"""
import subprocess as sp

from flask_script import Manager, Shell, Server as OldServer
from flask_migrate import MigrateCommand, Migrate

from Application import application as app, db, celery
from Application.auth.models import User

manager = Manager(app)
migrate = Migrate(app, db)

class Server(OldServer):

  def __call__(self, *args, **kwargs):
    if app.config["DEBUG"]:
      app.config["ASSETS_URL"] = "http://localhost:5001/static/"
      webpack_server = sp.Popen(["/usr/bin/node",
                                 "node_modules/webpack-dev-server/bin/webpack-dev-server.js",
                                 "--content-base", "../static",
                                 "--output-public-path", "http://localhost:5000/static/",
                                 "--inline",
                                 "--hot",
                                 "--port", "5001",
                                ], cwd="Application/app_src")
    super().__call__(*args, **kwargs)

def make_shell_context():
  import Application
  import Application.auth
  context = {"app": app, "db": db}
  for model in Application.public_models:
    context[model.__name__] = model
  for model in Application.auth.AdminModels:
    context[model.__name__] = model
  for table in Application.public_tables:
    context[table.name] = table
  return context

@manager.command
def create_user():
  """Create a superuser"""
  import getpass
  user = input("Username [{}]: ".format(getpass.getuser()))
  if not user:
    user = getpass.getuser()
  pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))
  p1, p2 = pprompt()
  while p1 != p2:
    print('Passwords do not match. Try again')
    p1, p2 = pprompt()

  User.create(username=user, password=p1, active=True, is_admin=True)
  print('Administrator account created for {}'.format(user))

@manager.command
def npm_install():
  sp.run(["/usr/bin/npm", "install"], cwd="Application/app_src", check=True)

@manager.command
def webpack_build():
  sp.run(["/usr/bin/node", "node_modules/webpack/bin/webpack.js"], cwd="spinneret/app_src", check=True)

@manager.command
def celery_refresh():
  celery.control.broadcast("pool_restart", arguments={"reload": True})

@manager.command
def celery_flush():
  celery.control.purge()

@manager.command
def celery_worker():
  sp.run(["celery", "worker", "-A", "application.celery"], check=True)

@manager.command
def celery_flower():
  sp.run(["celery", "flower", "-A", "application.celery"], check=True)

@manager.command
def run_uwsgi():
  sp.run(["uwsgi", "uwsgi.ini"], check=True)
manager.add_command('runserver', Server(threaded=True, port=5000, host="0.0.0.0"))
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()
