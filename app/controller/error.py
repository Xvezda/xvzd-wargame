#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask import Blueprint
from flask import render_template

from common.conf import pages


error_blueprint = Blueprint('error', __name__)

@error_blueprint.app_errorhandler(400)
def not_found(error):
  return render_template('400.html', error=error), 400

@error_blueprint.app_errorhandler(403)
def not_allowed(error):
  return render_template('403.html', error=error), 403

@error_blueprint.app_errorhandler(404)
def not_found(error):
  return render_template('404.html', error=error), 404

