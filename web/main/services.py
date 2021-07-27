from django.contrib.auth import get_user_model

from auth_app.utils import get_activate_key
from main.decorators import except_shell
from src.celery import app
from auth_app.tasks import send_information_email

User = get_user_model()


class CeleryService:

    @staticmethod
    def send_password_reset(data: dict):
        send_information_email.delay("Your reset e-mail", "auth_app/reset_password_sent.html",
                                     data.get("content"), data.get("to_email"))

    @staticmethod
    def send_email_confirm(user):
        key = get_activate_key(user)
        kwargs = {
            'template_name': "auth_app/success_registration.html",
            'subject': "Congrats!Here is your confirmation url!",
            'to_email': user.email,
            'context': {
                'user': user.get_full_name(),
                'activate_url': key,
            }
        }
        print(kwargs)
        send_information_email.delay(kwargs.get("subject"), kwargs.get("template_name"),
                                     kwargs.get("context"), kwargs.get("to_email"))


class UserService:

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email):
        return User.objects.get(email=email)
