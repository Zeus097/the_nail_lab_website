from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import ClientProfile
from services.models import BaseService

User = get_user_model()

class TestServiceDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create user because it requires authentication
        cls.client_user = User.objects.create_user(
            username='client',
            password='asd123',
            email='client@mail.com',
            is_client=True,
        )

        cls.service = BaseService.objects.create(
            name='Test Service',
            description='Test Description',
            price=100,
            duration=150,
        )

        cls.client_profile = ClientProfile.objects.get(user=cls.client_user)
        cls.url = reverse('service_details', kwargs={'pk': cls.service.pk})

    def setUp(self):
        self.client.login(username='client', password='asd123')

    def test_view_status_code_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # If there were no user, the status was going to be 302.

    def test_context_object_name(self):
        response = self.client.get(self.url)
        self.assertIn('service', response.context)
        self.assertEqual(response.context['service'], self.service)
