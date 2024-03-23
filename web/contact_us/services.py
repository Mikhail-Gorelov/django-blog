from django.conf import settings

from auth_app.tasks import send_information_email
from src.settings import ADMIN_EMAIL


class ContactUsService:
    @staticmethod
    def send_contact_us_email(feedback):
        user_data = ContactUsService.send_contact_us_email_user(feedback)
        send_information_email.delay(**user_data)
        admin_data = ContactUsService.send_contact_us_email_admin(feedback)
        send_information_email.delay(**admin_data)

    @staticmethod
    def send_contact_us_email_admin(feedback):
        return {
            "subject": "Feedback from " + feedback.name,
            "html_email_template_name": "emails/admin_email.html",
            "context": {
                "user": feedback.name,
                "to_email": ADMIN_EMAIL,
                "content": feedback.content,
            },
            "to_email": ADMIN_EMAIL,
        }

    @staticmethod
    def send_contact_us_email_user(feedback):
        return {
            "subject": "Thank you for your feedback",
            "html_email_template_name": "emails/user_email.html",
            "context": {
                "user": feedback.name,
            },
            "to_email": feedback.email,
        }
