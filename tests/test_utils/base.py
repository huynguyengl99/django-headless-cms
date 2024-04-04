from django.contrib.auth.models import User
from django.test import SimpleTestCase, TransactionTestCase
from django.test.utils import override_settings
from rest_framework.test import APITransactionTestCase

# Test helpers.


class TestBaseTransaction(TransactionTestCase):
    def _should_reload_connections(self):
        return False


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class UserMixin(SimpleTestCase):
    def setUp(self):
        super().setUp()
        self.user = User(username="test", is_staff=True, is_superuser=True)
        self.user.set_password("password")
        self.user.save()


class LoginMixin(UserMixin):

    def setUp(self):
        super().setUp()
        self.client.login(username="test", password="password")


class BaseTestCase(LoginMixin, TestBaseTransaction):
    pass


class BaseAPITestCase(LoginMixin, TestBaseTransaction, APITransactionTestCase):
    pass
