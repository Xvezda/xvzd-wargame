#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask import Blueprint
from flask import render_template

from common.conf import pages


error_blueprint = Blueprint('error', __name__)

@error_blueprint.app_errorhandler(400)
def not_found(error):
  context = {
    'title': 'Error 400',
    'current_page': '400',
    'pages': pages,
    'content': error.description
  }
  return render_template('skeleton.html', **context), 400


@error_blueprint.app_errorhandler(404)
def not_found(error):
  context = {
    'title': 'Error 404',
    'current_page': '404',
    'pages': pages
  }
  return render_template('skeleton.html', **context), 404


@error_blueprint.app_errorhandler(403)
def not_allowed(error):
  context = {
    'title': 'Error 403',
    'current_page': '403',
    'pages': pages
  }
  return render_template('skeleton.html', **context), 403

