#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask import Blueprint
from flask import abort
from flask import render_template
from flask import send_from_directory

from common.conf import pages
from common.func import check_hack, favicon_path


index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/favicon.ico')
def favicon():
  return send_from_directory(
    favicon_path(), 'favicon.ico', mimetype='image/vnd.microsoft.icon'
  )

@index_blueprint.route('/')
def main():
  return render_template('home.html')

@index_blueprint.route('/home')
def redir_home():
  return redirect('/', code=302)

