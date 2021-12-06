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


class FooTaskTestCase(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.celery_worker = start_worker(app, perform_ping_check=False)
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None, None, None)

    def setUp(self):
        super().setUp()
        self.task_add = tasks.add.delay(2, 2)
        self.results_add = self.task_add.get()

        self.task_mul = tasks.mul.delay(4, 4)
        self.results_mul = self.task_mul.get()

        # assert tasks.add.delay(2, 2).get(timeout=10) == 4
        # assert tasks.mul.delay(4, 4).get(timeout=10) == 16

    def test_add(self):
        assert self.task_add.state == "SUCCESS"

    def test_mul(self):
        assert self.task_mul.state == "SUCCESS"
