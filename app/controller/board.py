#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from sys import maxint
from flask import Blueprint
from flask import escape
from flask import redirect
from flask import request
from flask import session
from flask import current_app
from flask import abort

from common.conf import *
from common.func import giveme_flag
from common.func import render_template
from common.lib import handler
from common.lib import security
from model.board import get_article, write_article
from model.account import get_user_info
from model.message import send_message


boards = XVZD_BOARDS__
board_blueprint = Blueprint('board', __name__)

@board_blueprint.route('/about')
@handler.db_error_wrapper
def about():
  return render_template('about.html')


@board_blueprint.route('/pricing')
def pricing():
  return render_template('pricing.html')


@board_blueprint.route('/<board>/write')
@security.csrf_token_wrapper
def board_write(board):
  if board not in boards:
    return abort(400, '')
  return render_template('board_write.html', board=board)


@board_blueprint.route('/<board>/write-check', methods=['GET', 'POST'])
@handler.db_error_wrapper
@security.form_validate_wrapper(require=['title', 'content'])
@security.csrf_check_wrapper
def board_write_check(board):
  if board not in boards:
    return abort(400, '')

  if not session.get('is_logged'):
    return render_template('redirect.html', script="""
      <script>
        alert('You are not logged in!');
        location = '/login';
      </script>
    """), 403
  # Notice board admin only
  if (board == 'notice' and (session.get('user_id') != 'admin'
      or not session.get('is_admin') or request.remote_addr != '127.0.0.1')):
    return abort(403, 'Not that easy LOL')

  title = request.form['title'].replace('<', '').replace('>', '')
  content = request.form['content']

  uid = get_user_info(['uid'], {'id': session.get('user_id')}).get('uid')

  # Abort if input contains malicious payloads
  if security.check_hack(title, content):
    return abort(400, '')
  content = security.purify(content)

  if not uid:
    return abort(400, 'What the hell??')

  ip = request.remote_addr
  write_article(board, title, content, uid, ip)

  # Make bot check article
  if board == 'qna':
    from app import run_bot

    result = run_bot.delay()
    #result.wait()

  # Send flag if hacked
  if (board == 'notice' and title[:10].lower() == 'hacked by '):
    sender_uid = get_user_info(['uid'], {'id': 'admin'}).get('uid')

    target_id = title.lower().split()[-1]
    target_uid = get_user_info(['uid'], {'id': target_id}).get('uid')

    if sender_uid and target_uid:
      flag = giveme_flag()
      html = '''
        <img src="https://i.imgur.com/GYso5uF.jpg" class="img-fluid">
        <br>
        <p>%s</p>
      ''' % (flag)
      send_message(sender_uid, target_uid, 'HERE IS YOUR FLAG!', html, ip)

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

  return render_template(board+'.html', board=board, page=page)

