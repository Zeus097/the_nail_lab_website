from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import EmployeeBio
from services.models import BaseService

User = get_user_model()

class TestServiceListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ivan', email='ivan@test.com', password='asd123')
        self.employee = EmployeeBio.objects.create(user=self.user)
        self.client.login(username='ivan', email='ivan@test.com', password='asd123')

        # Creating services for 'test_services__pagination'
        for i in range(6):
            BaseService.objects.create(
                name=f"service {i}",
                description=f"Description {i}",
                price=100,
                duration=150
            )

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
