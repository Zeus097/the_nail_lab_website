from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import BaseUser


class BaseUserCreationTestCase(TestCase):
    def test_user_creation_with_valid_data(self):
        user = BaseUser(
            email='test@mail.com',
            username='ivan',
            password='asd034278',
            telephone_number='0897338846'
        )

        user.full_clean()
        user.save()

        self.assertIsNotNone(user)

    def test_user_creation_with_missing_password(self):
        user = BaseUser(
            email='test@mail.com',
            username='ivan',
            telephone_number='0897338846'
        )

        with self.assertRaises(ValidationError):
            user.full_clean()