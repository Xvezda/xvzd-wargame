#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask import Blueprint
from flask import render_template


board_blueprint = Blueprint('board', __name__)

@board_blueprint.route('/notice')
def notice():
  return render_template('notice.html')

@board_blueprint.route('/items')
def items():
  return render_template('items.html')

@board_blueprint.route('/support')
def support():
  return render_template('support.html')
