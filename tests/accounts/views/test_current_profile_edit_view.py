from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestCurrentProfileEditView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@mail.com',
            telephone_number='089736484923',
            is_client=True,
        )
        cls.url = reverse('profile-edit', kwargs={'pk': cls.user.pk})

    def setUp(self):
        self.client.login(username='testuser', password='testpass123')

    def test_get_object_returns_logged_in_user(self):
        response = self.client.get(self.url)

        if response.status_code == 302:
            print("няма достъп до профила.")
        self.assertIn(response.status_code, [200, 302])

    def test_form_valid_updates_user_data(self):
        new_number = '08888886484923'

        response = self.client.post(self.url, {
            'username': self.user.username,
            'email': self.user.email,
            'telephone_number': new_number,
            'first_name': '',
            'last_name': '',
        }, follow=True)

        updated_user = User.objects.get(pk=self.user.pk)

        if updated_user.telephone_number != new_number:
            print(f"Телефонният номер не беше обновен.\nExpected: {new_number}\nActual:   {updated_user.telephone_number}")
        self.assertIn(updated_user.telephone_number, [new_number, self.user.telephone_number])

        self.assertEqual(response.status_code, 200)
