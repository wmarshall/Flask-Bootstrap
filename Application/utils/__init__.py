# -*- coding: utf-8 -*-
""" Helper utilities and decorators. """

import random
from flask import flash, get_flashed_messages, jsonify

from .json import JSONEncoder

def flash_form_errors(form, category="warning"):
  """ Flash all errors for a form. """
  for field, errors in form.errors.items():
    for error in errors:
      flash("{0} - {1}".format(getattr(form, field).label.text, error), category)

def make_json_response(code=200, **kwargs):
  """ jsonify flashed messages """
  kwargs.update({"messages": get_flashed_messages(with_categories=True)})
  return jsonify(kwargs), code

def generate_token(length=8, alphabet="abcdefghijklmnopqrstuvwxyz0123456789"):
  """ Generate a random token of given length from the specified set of
    characters.  Not guaranteed to be unique.
  """
  return ''.join(random.choice(alphabet) for _ in range(length))

__all__ = ["flash_form_errors", "generate_token", "make_json_response", "JSONEncoder"]
