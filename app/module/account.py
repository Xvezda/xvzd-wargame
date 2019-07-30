from main import csrf_token

from flask import request
from flask import session
from flask import redirect
from flask import render_template
from flask import Blueprint

account = Blueprint('account', __name__)


@account.route('/logout')
def logout():
  if session.get('is_logged'):
    session.clear()
  return redirect('/', code=302)

@account.route('/login')
def login():
  context = {
    'title': 'Login',
    'current_page': 'login',
    'pages': pages
  }
  session['csrf_token'] = csrf_token()

  return render_template('skeleton.html', **context)

@account.route('/login-check', methods=['GET', 'POST'])
def login_check():
  if request.method == 'POST':
    if any([
        'csrf_token' not in request.form,
        'csrf_token' not in session,
        request.form.get('csrf_token') != session.get('csrf_token')]):
      return abort(400, 'CSRF Attack Detected!')
    session.pop('csrf_token')

    require = ['user_id', 'user_pw']
    if not all(field in request.form for field in require):
      return abort(400, 'Something is missing!')

    user_id = request.form['user_id'].strip()
    user_pw = request.form['user_pw'].strip()

    if check_hack(user_id+user_pw):
      return abort(400, '')

    cursor.execute('select name, password from xvzd_users where id = %s',
                   (user_id))

    result = cursor.fetchone()
    name = result[0] if result else None
    password = result[1] if result else None

    pw_hash = hashlib.sha512(user_pw.encode('utf-8')).hexdigest()
    if password == pw_hash:
      session['is_logged'] = True
      session['user_id'] = user_id
      session['user_name'] = name

      if user_id == 'admin':
        session['is_admin'] = True

      resp = make_response(redirect('/', code=302))
      if session.get('is_admin', False):
        # If admin
        # NOTE: Admin will set flag here
        resp.set_cookie('flag',
                        os.getenv('WARGAME_FLAG', 'NO_FLAG'))
      else:
        resp.set_cookie('flag', 'admin_has_real_flag_here')
      return resp
    else:
      return abort(400, """
        <script>alert('ID, PW not match!');history.back();</script>
      """)
  else:
    return redirect('/', code=302)

@account.route('/join')
def join():
  context = {
    'title': 'Join',
    'current_page': 'join',
    'pages': pages
  }
  session['csrf_token'] = csrf_token()

  return render_template('skeleton.html', **context)

@account.route('/join-check', methods=['GET', 'POST'])
def join_check():
  if request.method == 'POST':
    if any([
        'csrf_token' not in request.form,
        'csrf_token' not in session,
        request.form.get('csrf_token') != session.get('csrf_token')]):
      return abort(400, 'CSRF Attack Detected!')
    session.pop('csrf_token')

    require = ['user_id', 'user_name', 'user_pw']
    if not all(field in request.form for field in require):
      return abort(400, 'Something is missing!')

    user_id = request.form['user_id'].strip()[:0x80]
    user_name = request.form['user_name'].strip()[:0x80]
    user_pw = request.form['user_pw'].strip()[:0x80]

    user_pw = hashlib.sha512(user_pw.encode('utf-8')).hexdigest()

    try:
      cursor.execute('''
        insert into xvzd_users (id, name, password) values (%s, %s, %s)
      ''', (user_id, user_name, user_pw))
    except:
      return abort(400, """
        <script>alert('ID Already exists!');history.back();</script>
      """)
    conn.commit()

    return 'join', 200
  else:
    return redirect('/', code=302)

