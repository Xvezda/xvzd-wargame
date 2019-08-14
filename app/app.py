#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask_minify import minify

from common.conf import create_app
from common.conf import make_celery
from controller.account import account_blueprint
from controller.board import board_blueprint
from controller.index import index_blueprint
from controller.error import error_blueprint

import bot


app = create_app(__name__)

app.register_blueprint(account_blueprint)
app.register_blueprint(board_blueprint)
app.register_blueprint(error_blueprint)
app.register_blueprint(index_blueprint)

#minify(app=app)
app.config.update(
  CELERY_BROKER_URL='redis://127.0.0.1:6379',
  CELERY_RESULT_BACKEND='redis://127.0.0.1:6379'
)
celery = make_celery(app)

@celery.task()
def run_bot():
  bot.check_article()


if __name__ == "__main__":
  # Only for debugging while developing
  app.run(host='0.0.0.0', debug=True, port=8080)

