from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask import session
from flask import flash
from functools import wraps


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if session.get('logged_in', False):
            return func(*args, **kwargs)
        else:
            flash('You need login in')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def home():
    session['logged_in'] = session.get('logged_in', False)
    return render_template('home.html')


@app.route('/posts')
@login_required
def posts():
    return render_template('posts.html')


@app.route('/hello')
@login_required
def hello():
    return render_template('hello.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = "Invalid login or password. Try again!"
        else:
            session['logged_in'] = True
            return redirect(url_for('hello'))

    return render_template('login.html', error=error)


@app.route('/posts/<int:post_id>')
@login_required
def show_post(post_id):
    print(post_id)
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id
