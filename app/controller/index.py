#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import subprocess

from flask import Blueprint
from flask import redirect
from flask import send_from_directory

from common.func import static_path
from common.func import render_template


index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/favicon.ico')
def favicon():
  return send_from_directory(
    static_path(), 'favicon.ico', mimetype='image/vnd.microsoft.icon'
  )

@index_blueprint.route('/')
def main():
  chrome_version = subprocess.check_output(['chromedriver', '--version'])
  return render_template('home.html', chrome_version=chrome_version)

@index_blueprint.route('/home')
def redir_home():
  return redirect('/', code=302)

