from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import LogInWithEmail

User = get_user_model()

class LogInWithEmailBackendTest(TestCase):
    def setUp(self):
        self.backend = LogInWithEmail()
        self.user = User.objects.create_user(
            username='test',
            email='test@mail.com',
            password='asd123',
            is_active=True,
        )

        self.inactive_user = User.objects.create_user(
            username='test2',
            email='test2@mail.com',
            password='asd123321',
            is_active=False,
        )

    def test_successful_authentication_insensitive_email_case(self):
        user = self.backend.authenticate(
            request=None,
            username='tEst@mail.com',
            password='asd123',
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.pk, self.user.pk)

    def test_unsuccessful_authentication__wrong_password(self):
        user = self.backend.authenticate(
            request=None,
            username='tEst@mail.com',
            password='2231as41423d123',
        )
        self.assertIsNone(user)

    def test_unsuccessful_authentication__wrong_email(self):
        user = self.backend.authenticate(
            request=None,
            username='test5@mail.com',
            password='asd123',
        )
        self.assertIsNone(user)

    def test_unsuccessful_authentication__inactive_user(self):
        user = self.backend.authenticate(
            request=None,
            username='test2@mail.com',
            password='asd123321',
        )
        self.assertIsNone(user)
