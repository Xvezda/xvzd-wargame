#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from common.conf import create_app
from common.conf import make_celery
from controller.account import account_blueprint
from controller.message import message_blueprint
from controller.board import board_blueprint
from controller.index import index_blueprint
from controller.error import error_blueprint

import bot


app = create_app(__name__)

app.register_blueprint(account_blueprint)
app.register_blueprint(message_blueprint)
app.register_blueprint(board_blueprint)
app.register_blueprint(error_blueprint)
app.register_blueprint(index_blueprint)

# Celery setup
app.config.update(
  CELERY_BROKER_URL='redis://127.0.0.1:6379',
  CELERY_RESULT_BACKEND='redis://127.0.0.1:6379'
)
celery = make_celery(app)


@celery.task()
def run_bot():
  bot.check_article()


# Prevent app from caching
@app.after_request
def add_header(response):
  # No cache when html
  if response.content_type[:9].lower() == 'text/html':
    response.headers['Cache-Control'] = 'no-cache, no-store, ' + \
      'must-revalidate, public, max-age=0'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    # XSS prevention
    response.headers['X-Frame-Options'] = 'deny'
    response.headers['X-XSS-Protection'] = '1; mode=block'
  return response


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)

