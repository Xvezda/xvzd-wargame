#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from sys import maxint
from flask import Blueprint
from flask import abort
from flask import escape
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import current_app

from common.conf import *
from common.lib import handler
from common.lib import security
from model.board import get_article, write_article
from model.account import get_user_info

import model.board as mboard
import model.account as maccount


boards = XVZD_BOARDS__
board_blueprint = Blueprint('board', __name__)

context = {}
context['mboard'] = mboard
context['maccount'] = maccount

@board_blueprint.route('/about')
@handler.db_error_wrapper
def about():
  return render_template('about.html', **context)


@board_blueprint.route('/pricing')
def pricing():
  return render_template('pricing.html', **context)


@board_blueprint.route('/<board>/write')
@security.csrf_token_wrapper
def board_write(board):
  if board not in boards:
    return abort(400, '')
  return render_template('board_write.html', board=board, **context)


@board_blueprint.route('/<board>/write-check', methods=['GET', 'POST'])
@handler.db_error_wrapper
@security.form_validate_wrapper(require=['title', 'content'])
@security.csrf_check_wrapper
def board_write_check(board):
  if board not in boards:
    return abort(400, '')

  if not session.get('is_logged'):
    return abort(400, """
      <script>
        alert('You are not logged in!');
        location = '/login';
      </script>
    """)
  # Notice board admin only
  if (board == 'notice' and (session.get('user_id') != 'admin'
      or not session.get('is_admin') or request.remote_addr != '127.0.0.1')):
    return abort(400, 'Not that easy LOL')

  title = request.form['title']
  # line break to br tag
  content = request.form['content'].replace('\n', '<br>')
  # Let's limit length to 150
  # if board == 'qna' and len(content) > 250:
  #   return abort(400, 'Max length of content limited to 250 bytes!')
  uid = get_user_info(['uid'], {'id': session.get('user_id')}).get('uid')

  if security.check_hack(title, content):
    return abort(400, '')

  if not uid:
    return abort(400, 'What the hell??')

  ip = request.remote_addr
  write_article(board, title, content, uid, ip)

  # Make bot check article
  if board == 'qna':
    from app import run_bot

    result = run_bot.delay()
    #result.wait()

  return redirect('/'+board, code=302)


@board_blueprint.route('/<board>/<int:no>')
@handler.db_error_wrapper
def board_read(board, no):
  if (board not in boards or security.check_hack(board)
      or not security.is_valid(r'[a-zA-Z0-9_-]+', board)
      or no > maxint):
    return abort(400, '')
  article = get_article(board, no)
  if not article:
    return abort(404)

  # Check permission on qna board
  if board == 'qna':
    if not article.get('pinned'):
      user_id = get_user_info(['id'], {'uid': article.get('uid')}).get('id')
      is_writer = (session.get('user_id') == user_id)
      if not session.get('is_logged'):
        return abort(403, 'You are not logged in!')
      if (not session.get('is_admin') and request.remote_addr != '127.0.0.1'
          and not is_writer):
        return abort(403, 'You are not admin!')

  return render_template('board_read.html', article=article, board=board)


@board_blueprint.route('/notice', defaults={'board': 'notice', 'page': 1})
@board_blueprint.route('/qna', defaults={'board': 'qna', 'page': 1})
@board_blueprint.route('/forum', defaults={'board': 'forum', 'page': 1})
@board_blueprint.route('/<board>/page/<int:page>')
@handler.db_error_wrapper
def board_list(board, page):
  if (board not in boards or security.check_hack(board)
      or not security.is_valid(r'[a-zA-Z0-9_-]+', board)
      or page > maxint):
    return abort(400, '')

  return render_template(board+'.html', board=board, page=page, **context)

