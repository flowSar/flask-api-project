#!/usr/bin/python3
from flask import Flask, request, render_template, session, redirect
from flask_session import Session
from dbmanager import DbManager
import uuid



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'Root@890seceretkey'
Session(app)

dbManager = DbManager()

@app.route('/')
def home():
    all_posts = dbManager.get_all_posts()
    username = session.get('username')
    user_id = session.get('user_id')
    return render_template('home.html', posts=all_posts, username=username, user_id=user_id)

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form.get('password')
        user = dbManager.get_user(email, password)
        if user is not None:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            return redirect('/')
        print('user id why: ', user)
        return render_template('sign_in.html')
    else:
        if request.method == 'GET':
            if 'user_id' in session:
                return redirect('/')
        return render_template('sign_in.html')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user_id = str(uuid.uuid4())
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        session['user_id'] = user_id
        session['username'] = username
        count = dbManager.insert_user(user_id, username, email, password)
        if count > 0:
            return redirect('/')
        return render_template('sign_up.html')
    else:
        if 'user_id' in session:
            return redirect('/')
        return render_template('sign_up.html')


@app.route('/publish', methods=['GET','POST'])
def publish_post():
    try:
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            user_id = session.get('user_id')
            count = dbManager.insert_post(title, content, user_id=user_id)
            if count > 0:
                return redirect('/')
        else:
            return render_template('home.html')
    except Exception as e:
        print(e)
        return redirect('/')

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    # print('id:', type(post_id), post_id)
    user_id = session.get('user_id')
    dbManager.delete_post(post_id, user_id)
    return redirect('/')

@app.route('/update/<int:post_id>', methods=['POST'])
def update_post(post_id):

    title = request.form.get('title')
    content = request.form.get('content')
    user_id = session.get('user_id')
    dbManager.update_post(post_id, title, content, user_id)
    return redirect('/')

@app.route('/logout')
def log_out():
    session.clear()
    return redirect('signin')

if __name__ == '__main__':
    app.run(debug=True, port=1234)

