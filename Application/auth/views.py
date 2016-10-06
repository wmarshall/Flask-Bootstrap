# -*- coding: utf-8 -*-
"""
views.py
Manages login views
"""
from functools import wraps
from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, abort)
from flask_login import (login_user, login_required, logout_user,
                         current_user)

from ..utils import flash_form_errors, make_json_response

from .forms import LoginForm, CreateUserForm, EditUserForm, ChangePasswordForm
from .models import User

blueprint = Blueprint("auth", __name__, url_prefix='/auth',
                      static_folder="../static")

user_view = User.register_rest_view(blueprint)

def role_required(role):
  """ Fails requests if the user does not have the specified role """
  def wrapper(wrapped):
    """enforces role_required"""
    @wraps(wrapped)
    def f(*args, **kwargs):
      """dummy wrapped function"""
      if current_user.has_role(role):
        return wrapped(*args, **kwargs)
      else:
        flash("You do not have the {role} role".format(role="role"), "warning")
        abort(403)
    return f
  return wrapper

@blueprint.route("/login/", methods=["GET", "POST"])
def login():
  """Log a user in"""
  form = LoginForm(request.form)
  if request.method == 'POST':
    if form.validate_on_submit():
      login_user(form.user)
      flash("You are logged in.", 'success')
      redirect_url = request.args.get("next") or url_for("main.dashboard")
      return make_json_response(redirect=redirect_url)
    else:
      flash_form_errors(form)
      abort(403)
  return render_template("auth/login.html", form=form)

@blueprint.route('/logout/')
@login_required
def logout():
  logout_user()
  flash('You are logged out.', 'info')
  return redirect(url_for('auth.login'))

@blueprint.route("/change-password/", methods=["GET", "POST"])
@login_required
def change_password():
  form = ChangePasswordForm(request.form)
  if form.is_submitted():
    if form.validate():
      form.user.set_password(form.password.data)
      form.user.save()
      flash("Password successfully changed.", 'success')
      return make_json_response()
    else:
      flash_form_errors(form)
      abort(400)
  return render_template("auth/change-password.html", form=form)

@blueprint.route('/users/')
@role_required('orgadmin')
def user_list():
  # User can only manage within their own organization
  users = (User.query
           .order_by(User.username)
           .all())
  return render_template("auth/user-list.html", users=users)

@blueprint.route("/users/add", methods=['GET', 'POST'])
@role_required('orgadmin')
def create_user():
  form = CreateUserForm(request.form)
  if form.is_submitted():
    if form.validate():
      new_user = User.create(username=form.username.data,
                             full_name=form.full_name.data,
                             password=form.password.data,
                             active=True)
      flash("'{username}' account created.".format(username=new_user.username), 'success')
      return make_json_response()
    else:
      flash_form_errors(form)
      abort(400)
  return render_template('auth/user-add.html', form=form)

@blueprint.route("/users/<username>", methods=['GET', 'POST'])
@role_required('orgadmin')
def edit_user(username):
  user = User.query.filter_by(id=username).one()
  form = EditUserForm(request.form, user)
  if form.is_submitted():
    if form.validate():
      user.full_name = form.full_name.data
      if form.password.data:
        user.set_password(form.password.data)
      user.active = form.active.data == 'True'
      user.is_admin = form.is_admin.data == 'True'
      user.save()
      return make_json_response()
    else:
      flash_form_errors(form)
      abort(400)
  return render_template('auth/user-edit.html', form=form, user=user)
