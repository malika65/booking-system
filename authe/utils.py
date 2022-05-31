from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken

from authe.models import User
from main.celery import app


@app.task
def send_email(user, current_site):
    token = RefreshToken.for_user(user).access_token
    relativeLink = '/authe/email-verify/'
    absurl = 'http://'+current_site+relativeLink+str(token)
    email_body = 'Hi '+user.email + \
            ' Use the link below to verify your email \n' + absurl
    data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    email.send()


@app.task
def send_code_to_email(user_id, code):
    user = User.objects.filter(id=user_id).first()
    email_body = code
    data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Ваш код для подтверждения почты'}
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    email.send()


@app.task
def send_reset_email(data):
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    email.send()
