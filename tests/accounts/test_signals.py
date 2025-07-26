from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import ClientProfile, EmployeeBio

User = get_user_model()

class TestUserProfileSignals(TestCase):
    def test_create_non_employee_sets_is_client(self):
        user = User.objects.create_user(
            username='test',
            email='test@mail.com',
            password='asd123',
            is_employee=False,
            is_client=False,
        )

        # Check after the signal is triggered
        user.refresh_from_db()

        self.assertTrue(user.is_client)

    def test_create_non_employee__and_creates_client_profile(self):
        user = User.objects.create_user(
            username='test',
            email='test@mail.com',
            password='asd123',
            is_employee=False,
            is_client=False,
        )

        client = ClientProfile.objects.filter(user=user)
        self.assertTrue(client.exists())

    def test_create_employee_creates_employee_bio(self):
        user = User.objects.create_user(
            username='test1',
            email='test1@example.com',
            password='asd1233215',
            is_employee=True,
            is_client=False
        )

        emp_bio = EmployeeBio.objects.filter(user=user).first()
        self.assertIsNotNone(emp_bio)
        self.assertEqual(emp_bio.name, user.username)

    def test_client_profile_created_for_client_user(self):
        user = User.objects.create_user(
            username='client1',
            email='client1@example.com',
            password='d12332',
            is_employee=False,
            is_client=True
        )
        client_profile = ClientProfile.objects.filter(user=user)
        self.assertTrue(client_profile.exists())
