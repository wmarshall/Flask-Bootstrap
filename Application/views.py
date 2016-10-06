# -*- coding: utf-8 -*-
"""Main UI section."""
from flask import Blueprint, render_template
from flask_login import login_required

from .models import public_models

blueprint = Blueprint('main', __name__, static_folder="../static")

for model in public_models:
  # print(model)
  model.register_rest_view(blueprint)

###
### The UI application is driven by something else, so a single server-driven
### template and a few helpers are all that is needed, in addition to the API.
###

@blueprint.route("/", methods=["GET"])
@login_required
def dashboard():
  """renders app dashboard"""
  context = {}
  return render_template("dashboard.html", **context)

