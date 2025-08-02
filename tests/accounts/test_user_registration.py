from django.test import TestCase
from django.urls import reverse
from accounts.models import BaseUser


class UserRegistrationTest(TestCase):
    def test_user_registration_with_spaced_phone(self):
        url = reverse('register')
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'telephone_number': '359 88 712 3456',
            'password1': 'TesttPassasd123321',
            'password2': 'TesttPassasd123321',
        }

        response = self.client.post(url, data=user_data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(BaseUser.objects.filter(username='testuser').exists())
        user = BaseUser.objects.get(username='testuser')

        self.assertEqual(user.telephone_number, '359887123456')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

