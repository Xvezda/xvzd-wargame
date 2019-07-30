#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask import Blueprint
from flask import abort
from flask import render_template
from flask import send_from_directory

from common.conf import pages
from common.func import check_hack

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/favicon.ico')
def favicon():
  return send_from_directory(
    os.path.join(app.root_path, 'static'),
    'favicon.ico', mimetype='image/vnd.microsoft.icon'
  )

@index_blueprint.route('/home')
def redir_home():
  return redirect('/', code=302)

@index_blueprint.route('/')
@index_blueprint.route('/<page>')
def main(page='home'):
  if check_hack(page):
    return abort(400, '')
  context = {
    'title': page.title(),
    'current_page': page,
    'pages': pages
  }
  return render_template('skeleton.html', **context)

