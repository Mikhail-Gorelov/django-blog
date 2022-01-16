from django.test import TestCase
from django.test import TransactionTestCase
from main import tasks
from celery.contrib.testing.worker import start_worker
from main.models import User
from src.celery import app


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('user@test.com', 'pass')

    def test_user_str(self):
        email = str(self.user)
        self.assertEqual(email, 'user@test.com')
