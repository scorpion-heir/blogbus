from app import db
from flask import render_template, request, redirect, url_for, flash #current_app as app, not needed here, becase we don't need to reference anything from the app instance, we only reference main instance  
from app.blueprints.auth.models import User
from app.blueprints.blog.models import Post 
from flask_login import login_user, current_user, logout_user, login_required 
from .import bp as main_bp
from .email import send_email





@main_bp.route('/')
def home():
    if current_user.is_authenticated:
        posts = current_user.followed_posts().all()
    else:
        posts = [] 
    context = {
        'user': current_user,
        'posts': posts 
       
    }
    return render_template('home.html', **context)

@main_bp.route('/profile')
@login_required
def profile():
    context = {
        'posts': [p for p in Post.query.order_by(Post.date_created.desc()).all() if p.user_id == current_user.id]
    }
    return render_template('profile.html', **context)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        form_data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'budget': request.form['budget'],
            'message': request.form['message'],
        }
        send_email(form_data)
        flash('Thank you for sending your inquiry. We will contact you shortly!', 'primary')
        return redirect(url_for('main.contact'))
    return render_template('contact.html')

@main_bp.route('/explore') 
@login_required
def explore(): 
    context = {
        'users': [user for user in User.query.all() if current_user.id != user.id ] # not showing myself as followers on explore page
    }
    return render_template('explore.html', **context)


