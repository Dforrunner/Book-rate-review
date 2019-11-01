from flask import current_app as app
from flask_mail import Message
from ext import mail


if not app.config['MAIL_DEFAULT_SENDER']:
    print("Mail default sender not found")


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    try:
        mail.send(msg)
    except ConnectionRefusedError:
        print("Email not sent")
