from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import ClientProfile
from services.models import BaseService

User = get_user_model()

class TestServiceDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_user = User.objects.create_user(
            username='client',
            password='asd123',
            email='client@mail.com',
            is_client=True,
            telephone_number='0899123456',
        )

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        image = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')

        cls.service = BaseService.objects.create(
            name='Test Service',
            description='Test Description',
            price=100,
            duration=150,
        )
        cls.service.service_photo.save('small.gif', image, save=True)

        cls.client_profile = ClientProfile.objects.get(user=cls.client_user)
        cls.url = reverse('service_details', kwargs={'pk': cls.service.pk})

    def setUp(self):
        self.client.login(username='client', password='asd123')

    def test_view_status_code_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_context_object_name(self):
        response = self.client.get(self.url)
        self.assertIn('service', response.context)
        self.assertEqual(response.context['service'], self.service)
