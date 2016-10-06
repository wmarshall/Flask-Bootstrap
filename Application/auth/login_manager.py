"""
login_manager.py
defines login manager
"""
from flask import render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user

from .models import User

login_manager = LoginManager()

login_manager.login_view = 'users.login'

@login_manager.unauthorized_handler
def unauthorized():
  """Try to make the user login"""
  if current_user and current_user.is_authenticated:
    return render_template('403.html')
  else:
    flash("Please login to access this resource", "warning")
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(username):
  """Load users given string uid"""
  return User.query.filter(User.username == username).first_or_404()
"""
login_manager.py
defines login manager
"""
from flask import render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user

from .models import User

login_manager = LoginManager()

login_manager.login_view = 'users.login'

@login_manager.unauthorized_handler
def unauthorized():
  """Try to make the user login"""
  if current_user and current_user.is_authenticated:
    return render_template('403.html')
  else:
    flash("Please login to access this resource", "warning")
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(username):
  """Load users given string uid"""
  return User.query.filter(User.username == username).first_or_404()
