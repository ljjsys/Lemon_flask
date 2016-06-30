from flask import render_template, request, redirect, flash, session
from . import main
from ..models import User
from flask.ext.login import login_user, logout_user, login_required
from .. import login_manager

@main.route('/', methods=['POST', 'GET'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        _username = request.form['username']
        _password = request.form['password']
        print (_username, _password)
        user = User.query.filter_by(user_name = _username).first()

        if user is not None and user.verify_password(_password):
            login_user(user)
            session['username'] = user.user_name
            print(user.id, user.user_name, user.password_hash)
            print(session)
            # return redirect('/Dashboard')
            return redirect(request.args.get('next') or '/Dashboard')

        flash('Invalid username or password.')
        return render_template('login.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
    # return 'Unauthorized: You have no access to this page.'
    return render_template('Errors/unauthorized.html')


@main.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@main.route('/Dashboard')
@login_required
def dashboard():
    return render_template('Dashboard.html', user_name = session.get('username'))
