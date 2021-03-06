#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask import Blueprint
from common.func import render_template


error_blueprint = Blueprint('error', __name__)

@error_blueprint.app_errorhandler(400)
def bad_request(error):
  return render_template('400.html', error=error), 400

@error_blueprint.app_errorhandler(403)
def not_allowed(error):
  return render_template('403.html', error=error), 403

@error_blueprint.app_errorhandler(404)
def not_found(error):
  return render_template('404.html', error=error), 404

@error_blueprint.app_errorhandler(503)
def service_unavailable(error):
  return render_template('503.html', error=error), 503

