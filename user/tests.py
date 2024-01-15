from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.

class Test(TestCase):
    def test_1(self):
        self.assertEquals(1, 1)

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username="test",
            password=make_password("password"),
            first_name="q",
            last_name="q",
            is_superuser="0",
            is_active="1",
            is_staff="0",
        )

    def test_login(self):
        response = self.client.post('/user/login', data=dict(
            username="test",
            password="password"))

        self.assertEquals(response.status_code, 200)