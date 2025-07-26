from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestCurrentProfileEditView(TestCase):
    # Testing only UpdateView logic

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@mail.com',
            telephone_number= '089736484923',
            is_client=True
        )
        cls.url = reverse('profile-edit', kwargs={'pk': cls.user.pk})

    def setUp(self):
        self.client.login(username='testuser', password='testpass123')

    def test_get_object_returns_logged_in_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_form_valid_updates_user_data(self):
        new_telephone_number = '08888886484923'
        response = self.client.post(
            self.url,
            {
                'username': 'testuser',
                'email': 'test@mail.com',
                'first_name': '',
                'last_name': '',
                'telephone_number': new_telephone_number,
            },
            follow=True
        )

        self.user.refresh_from_db()

        self.assertEqual(self.user.telephone_number, new_telephone_number)
        self.assertRedirects(response, reverse('profile-details', kwargs={'pk': self.user.pk}))

