from flask_mail import Message
from app import mail
from flask import render_template, current_app
from threading import Thread


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # current_app is a context-aware variable that is tied to the
    # thread that is handling the client request. In a different thread,
    # current_app would not have a value assigned. Passing it directly
    # as an argument to the thread object would not have worked either,
    # because current_app is really a "proxy object" that is dynamically
    # mapped to the application instance. So passing the proxy object would
    # be the same as using current_app directly in the thread. What I needed
    # to do is access the real application instance that is stored inside
    # the proxy object, and pass that as the app argument.
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_async_email(app_, msg_):
    with app_.app_context():
        mail.send(msg_)


def send_password_reset_email(user_):
    token_ = user_.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user_.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user_, token=token_),
               html_body=render_template('email/reset_password.html', user=user_, token=token_))

