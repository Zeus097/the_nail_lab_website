from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import ClientProfile, EmployeeBio

User = get_user_model()


class TestCurrentProfileDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.client_user = User.objects.create_user(
            username='client',
            password='asd123',
            email='client@mail.com',
            is_client=True,
        )

        cls.employee_user = User.objects.create_user(
            username='employee',
            password='asd123321',
            email='employee@mail.com',
            is_employee=True,
        )


        cls.other_user = User.objects.create_user(
            username='otheruser',
            password='asd123678',
            email='otheruser@mail.com',
            is_client=False,
            is_employee=False,
        )


        cls.client_profile = ClientProfile.objects.get(user=cls.client_user)
        cls.employee_profile = EmployeeBio.objects.get(user=cls.employee_user)
        cls.url = reverse('profile-details', kwargs={'pk': cls.client_user.pk})

    def test_redirect_anonymous_user(self):
        # hits the protected URL (profile-details)
        url = reverse('profile-details', kwargs={'pk': self.client_user.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.url)

    def test_redirect_authenticated_user(self):
        self.client.login(username='employee', password='asd123321')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_details.html')

    def test_user_without_profile(self):
        self.client.login(username='random', password='axxxx1')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
