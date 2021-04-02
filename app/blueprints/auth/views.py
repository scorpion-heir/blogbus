import os 
from flask import request, redirect, url_for, render_template, flash, jsonify, session
from app.blueprints.auth.models import User
from flask_login import login_user, logout_user, current_user, login_required
from app.blueprints.auth import bp as auth_bp 
from app import db, oauth
import json
from authlib.integrations.flask_client import OAuth 



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_email = request.form['email']
        form_password = request.form['password']
        
        user = User.query.filter_by(email=form_email).first()
        
        if user is not None and user.verify_password_hash(form_password):
            login_user(user) # allow log a user in, pass in the user info 
            flash('User successfully logged in', 'success') #has to be displayed using jinja 
            return redirect(url_for('main.home'))

        flash('There was an error logging in. Try again.', 'danger')
        return redirect(url_for('auth.login'))
        
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST']) #by default = GET, read/get html on server to display on browser, post info to our server in return 
def register():
    if request.method == 'POST':
        res = request.form
        if res['confirm_password'] == res['password']:
            u = User(first_name=res['first_name'], last_name=res['last_name'], password=res['password'], email = res['email'])
            u.save()
        return redirect(url_for('auth.login'))
        print(res) #only print if we 'POST' try to send form data 
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('User logged out successfully', 'info') #info is blue color
    return redirect(url_for('auth.login'))

@auth_bp.route('/follow')
@login_required
def follow():
    user_id = request.args.get('user_id')
    u = User.query.get(user_id)

    current_user.follow(u)
    flash(f'You have followed the {u.first_name} {u.last_name}', 'success')
    return redirect(url_for('main.explore'))

@auth_bp.route('/unfollow')
@login_required
def unfollow():
    user_email = request.args.get('email')
    u = User.query.filter_by(email=user_email).first()

    current_user.unfollow(u)
    flash(f'You have unfollowed the {u.first_name} {u.last_name}', 'info')
    return redirect(url_for('main.explore'))

@auth_bp.route('/update', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        form = request.form 
        if form['password'] and form['confirm_password']:
            if form['password'] == form['confirm_password']:
                user.password = form['password']
                user.create_password_hash(user.password)
        user.first_name = form['first_name']
        user.last_name = form['last_name']

        db.session.commit()
        flash("User's information has updated successfully", 'success')
    return redirect(url_for('main.profile'))



google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None, 
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'},
)

@auth_bp.route('/google-auth')
def google_auth():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.authorize', _external = True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = oauth.google.authorize_access_token()
    response = google.get('userinfo')
    user_info = response.json()
    user = oauth.google.userinfo()
    session['profile'] = user_info

    user = User.query.filter_by(email = user_info['email']).first()
    if user: 
        user.first_name = user_info['given_name']
        user.last_name = user_info['family_name']
        user.email = user_info['email']
        user.g_auth_verify = user_info['verified_email']

        db.session.add(user)
        db.session.commit()
        login_user(user)
        session.permanent = True
        return redirect(url_for('main.home'))

    else: 
        g_first_name = user_info['given_name']
        g_last_name = user_info['family_name']
        g_email = user_info['email']
        g_verified = user_info['verified_email']

        user = User(
            first_name = g_first_name,
            last_name = g_last_name,
            email = g_email,
            g_auth_verify = g_verified 
        )

        db.session.add(user)
        db.session.commit()
        session.permanent = True
        login_user(user) 
        return redirect(url_for('main.home'))

    print(user_info)
    return redirect(url_for('main.home'))