import re
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from django.core import mail

User = get_user_model()

# Create your tests here.
locmem_email_backend = override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CELERY_TASK_ALWAYS_EAGER=True,
)


class AuthTestCase(APITestCase):
    @locmem_email_backend
    def test_sign_up_flow(self):
        test_data = {
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "password1": "stringstring",
            "password2": "stringstring",
            "birthday": "2021-11-23",
            "gender": 0
        }
        sign_in_data = {
            "email": "user@example.com",
            "password": "stringstring",
        }
        response = self.client.post(reverse('auth_app:api_sign_up'), test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        user = User.objects.get(email='user@example.com')
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        pattern = r"(?P<url>https?://[^\s]+/auth/verify-email/[^\s]+[\r\n])" + r"([^\r\n]+/)"
        result = re.findall(pattern, str(message.message()))
        final_pattern = result[0][0].rstrip() + result[0][1]
        if not final_pattern:
            self.assertTrue(final_pattern, 'wrong url pattern')
        data = {
            "key": str(final_pattern.split('/')[5]).replace('=', '')
        }
        response_verify = self.client.post(reverse('auth_app:api_sign_up_verify'), data, format='json')
        self.assertNotEqual(response_verify.status_code, status.HTTP_404_NOT_FOUND)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        sign_in = self.client.post(reverse('auth_app:api_login'), sign_in_data)
        self.assertEqual(sign_in.status_code, status.HTTP_200_OK)

    @locmem_email_backend
    def test_forgot_password_flow(self):
        user_data = {
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "is_active": True,
        }
        password_reset_data = {
            "email": "user@example.com",
        }
        user = User.objects.create(**user_data)
        user.emailaddress_set.create(email=user.email, verified=True, primary=True)
        # EmailAddress.objects.create(email=user_data['email'], user=user, verified=True, primary=True)
        self.assertTrue(user.is_active)
        password_reset = self.client.post(reverse('auth_app:api_forgot_password'), password_reset_data)
        self.assertEqual(password_reset.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        pattern = r"(?P<url>https?://[^\s]+/auth/[^\s]+[\r\n])" + r"([^\r\n]+/)"
        result = re.findall(pattern, str(message.message()))
        final_pattern = str(result[0][0].rstrip() + result[0][1]).split('t/')[1][:-1]
        uid = final_pattern.split('/')[0]
        token = final_pattern.split('/')[1]
        change_password_using_credentials = {
            "new_password1": "stringstring",
            "new_password2": "stringstring",
            "uid": uid,
            "token": token
        }
        password_reset_confirm = self.client.post(
            reverse('auth_app:password_reset_confirm_email'), change_password_using_credentials)
        self.assertEqual(password_reset_confirm.status_code, status.HTTP_200_OK)
        sign_in_data = {
            "email": "user@example.com",
            "password": "stringstring",
        }
        login = self.client.post(reverse('auth_app:api_login'), sign_in_data)
        self.assertEqual(login.status_code, status.HTTP_200_OK, login.data)
