from flask_mail import Message
from flask import render_template, current_app as app
from app import mail 

def send_email(data):
    msg = Message(data['message'], sender=data['email'], recipients=[app.config.get('MAIL_USERNAME')])
    msg.html = render_template('email.html', sender=data)
    # print(msg)  
    mail.send(msg)
