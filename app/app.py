#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask_minify import minify

from common.conf import create_app
from controller.account import account_blueprint
from controller.board import board_blueprint
from controller.index import index_blueprint
from controller.error import error_blueprint


app = create_app(__name__)

app.register_blueprint(account_blueprint)
app.register_blueprint(board_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(error_blueprint)

if __name__ == "__main__":
  # Only for debugging while developing
  app.run(host='0.0.0.0', debug=True, port=8080)

