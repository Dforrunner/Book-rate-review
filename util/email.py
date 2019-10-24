from flask import Flask
from config import Config
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

if not app.config['MAIL_DEFAULT_SENDER']:
    print("Mail default sender not found")


def send_email(to, subject, template):
    with app.app_context():
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