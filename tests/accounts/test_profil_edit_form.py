from django.test import TestCase
from accounts.models import BaseUser, EmployeeBio
from accounts.forms import ProfileEditForm

class ProfileEditFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.employee_user = BaseUser.objects.create_user(
            username='employee_user',
            email='employee@mail.com',
            password='asd123',
            is_employee=True,
            telephone_number='0888123456',
        )

        cls.employee_bio, created = EmployeeBio.objects.get_or_create(user=cls.employee_user)
        cls.employee_bio.biography = 'Old bio'
        cls.employee_bio.save()

        cls.client_user = BaseUser.objects.create_user(
            username='client_user',
            email='client@mail.com',
            password='asd321',
            is_client=True,
            telephone_number='0888000000',
        )

    def test_employee_profile_update_with_biography(self):
        form_data = {
            'username': 'employee_user_updated',
            'email': 'emp_updated@example.com',
            'telephone_number': '0888123456',
            'first_name': 'Ivan',
            'last_name': 'Petrov',
            'biography': 'This is my new bio',
        }

        form = ProfileEditForm(
            data=form_data,
            instance=self.employee_user
        )

        self.assertTrue(form.is_valid())
        user = form.save()

        self.employee_bio.refresh_from_db()

        self.assertEqual(user.username, 'employee_user_updated')
        self.assertEqual(self.employee_bio.biography, 'This is my new bio')

    def test_client_profile_update_biography_ignored__for_non_employees(self):
        form_data = {
            'username': 'client_user_updated',
            'email': 'client_updated@example.com',
            'telephone_number': '0888123456',
            'first_name': 'Maria',
            'last_name': 'Ivanova',
            'biography': 'hi!',
        }

        form = ProfileEditForm(
            data=form_data,
            instance=self.client_user
        )

        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertFalse(hasattr(user, 'employeebio'))

    def test_invalid__missing_username__required_field(self):
        form_data = {
            'email': 'random@example.com',
            'telephone_number': '0888123456',
            'first_name': 'Test',
            'last_name': 'User',
            'biography': 'hello',
        }

        form = ProfileEditForm(data=form_data, instance=self.employee_user)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

