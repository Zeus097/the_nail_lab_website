from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import EmployeeBio, ClientProfile, BaseUser
from appointments.models import Appointment
from services.models import BaseService

User = get_user_model()

class TestHomePageView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('homepage')

        cls.service = BaseService.objects.create(
            name='test_service',
            duration=120,
            price=100
        )

        cls.client_user = User.objects.create_user(
            username='client',
            email='client@mail.com',
            password='123asd',
            is_client=True,
            telephone_number='08971112346',
        )

        cls.employee_user = User.objects.create_user(
            username='employee',
            email='employee@mail.com',
            password='asd123',
            telephone_number='0897122237',
            is_employee=True
        )

        cls.admin_client = User.objects.create_superuser(
            username='admin',
            email='admin@mail.com',
            password='asd123534dgd',
            telephone_number='0899123456',
        )

        cls.client_profile = ClientProfile.objects.get(user=cls.client_user)
        cls.employee_profile = EmployeeBio.objects.get(user=cls.employee_user)

    def test_anonymous_user_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/home_no_profile.html')

    def test_authenticated_user_template(self):
        User.objects.create_user(
            username='testuser',
            email='test@mail.com',
            password='asd123',
            telephone_number='0888123456',
        )
        self.client.login(username='testuser', password='asd123')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/base.html')

    def test_client_gets_their_appointments(self):
        self.client.login(username='client', password='123asd')

        Appointment.objects.create(
            employee=self.employee_profile,
            client=self.client_profile,
            date=date.today(),
            start_time='11:00',
            service=self.service,
        )

        # CONTEXT
        response = self.client.get(self.url)
        context = response.context

        self.assertIn('appointment_list', context)
        self.assertEqual(len(context['appointment_list']), 1)

        # Check the status
        self.assertTrue(response.wsgi_request.user.is_client)
        self.assertFalse(response.wsgi_request.user.is_employee)

    def test_employee_gets_their_appointments(self):
        self.client.login(username='employee', password='asd123')

        Appointment.objects.create(
            employee=self.employee_profile,
            client=self.client_profile,
            date=date.today(),
            start_time='11:00',
            service=self.service,
        )

        # CONTEXT
        response = self.client.get(self.url)
        context = response.context

        # CONTEXT keys
        self.assertIn('is_employee', context)
        self.assertIn('is_admin', context)

        self.assertIn('appointment_list', context)
        self.assertEqual(len(context['appointment_list']), 1)

        # Check the keys
        self.assertTrue(context.get('is_employee'))
        self.assertFalse(context.get('is_admin'))


        # Check the status
        self.assertTrue(response.wsgi_request.user.is_employee)
        self.assertFalse(response.wsgi_request.user.is_client)
        self.assertFalse(response.wsgi_request.user.is_superuser)

    def test_admin__context_view_case(self):
        self.client.login(username='admin', password='asd123534dgd')

        # Testing with appointment because the admin can see appointments
        Appointment.objects.create(
            employee=self.employee_profile,
            client=self.client_profile,
            date=date.today(),
            start_time='11:00',
            service=self.service,
        )

        # CONTEXT
        response = self.client.get(self.url)
        context = response.context

        # CONTEXT keys
        self.assertIn('is_admin', context)

        self.assertIn('appointment_list', context)
        self.assertEqual(len(context['appointment_list']), 1)

        # Check the keys
        self.assertTrue(context.get('is_admin'))

        # Check the status
        self.assertFalse(response.wsgi_request.user.is_employee)
        self.assertTrue(response.wsgi_request.user.is_client)
        self.assertTrue(response.wsgi_request.user.is_superuser)
