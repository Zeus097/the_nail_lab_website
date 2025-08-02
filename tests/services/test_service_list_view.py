from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import EmployeeBio
from services.models import BaseService

User = get_user_model()

class TestServiceListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ivan',
            email='ivan@test.com',
            password='asd123',
            telephone_number='0899123456',
        )
        self.employee = EmployeeBio.objects.create(user=self.user)
        self.client.login(username='ivan', password='asd123')

        # Dummy GIF image bytes
        self.small_gif_bytes = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        # Creating services for 'test_services__pagination' with dummy image
        for i in range(6):
            service = BaseService.objects.create(
                name=f"service {i}",
                description=f"Description {i}",
                price=100,
                duration=150
            )
            # Create a fresh SimpleUploadedFile every time!
            image = SimpleUploadedFile('small.gif', self.small_gif_bytes, content_type='image/gif')
            service.service_photo.save('small.gif', image, save=True)

    def test_services_view_status_code(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)

    def test_services__pagination(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('services'))
        response.render()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['services']), 4)

    def test_services_view_uses_correct_template(self):
        response = self.client.get(reverse('services'))
        self.assertTemplateUsed(response, 'services/services_page.html')
