from flask import Flask, render_template
from flask_minify import minify
from flaskext.mysql import MySQL

app = Flask(__name__)
#minify(app=app)

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'mysql'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route("/")
def main():
  return render_template('skeleton.html')
  #return "Hello World from Flask"

if __name__ == "__main__":
  # Only for debugging while developing
  app.run(host='0.0.0.0', debug=True, port=8080)
