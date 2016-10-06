# -*- coding: utf-8 -*-
""" Define our asset bundles for front-end minification """
from os import path
import subprocess as sp

from flask import redirect, request
from flask_webpack import Webpack


class MyWebpack(Webpack):
  def init_app(self, app):
    def redirect_static():
      if request.full_path.startswith(app.static_url_path):
        dev_server_url = app.config["ASSETS_URL"] + request.full_path[len(app.static_url_path):]
        return redirect(dev_server_url, code=301)
    if app.config["DEBUG"]:
      app.before_request(redirect_static)
    if not path.exists(app.config["WEBPACK_MANIFEST_PATH"]):
      sp.run(["/usr/bin/node", "node_modules/webpack/bin/webpack.js"], cwd="spinneret/app_src", check=True)
    super().init_app(app)

webpack = MyWebpack()

__all__ = ["webpack"]
