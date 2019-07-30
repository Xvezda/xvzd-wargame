#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>


import re
import os
import hashlib
import base64

from flask import Flask
from flask import session
from flask import abort
from flask import render_template, request, redirect, escape
from flask import make_response
from flask_minify import minify
from flaskext.mysql import MySQL

from common.db import mysql, db_setup
from common.conf import pages, create_app
from common.func import csrf_token, check_hack
from module.index import index_blueprint
from module.error import error_blueprint
from module.account import account_blueprint


app = create_app(__name__)
app.register_blueprint(error_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(account_blueprint)



if __name__ == "__main__":
  # Only for debugging while developing
  app.run(host='0.0.0.0', debug=True, port=8080)
  # Close mysql connection
  cursor.close()
  conn.close()
