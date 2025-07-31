from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import EmployeeBio


User = get_user_model()


class CurrentProfileDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ivan',
            email='ivan@test.com',
            password='asd123',
            telephone_number='0899123456'
        )
        self.employee = EmployeeBio.objects.create(user=self.user)
        self.client.login(username='ivan', email='ivan@test.com', password='asd123')

    def test_delete_confirmation_page(self):
        url = reverse('profile-delete', args=[self.employee.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_delete.html')

    def test_redirect_after_deletion(self):
        url = reverse('profile-delete', args=[self.employee.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('homepage'))