from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from accounts.models import ClientProfile, EmployeeBio
from services.models import BaseService
from appointments.models import Appointment

User = get_user_model()


class AppointmentCreateViewTests(TestCase):
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

        cls.service = BaseService.objects.create(
            name='Service 1',
            price=100,
            duration=150,
        )


        cls.client_profile = ClientProfile.objects.get(user=cls.client_user)
        cls.employee_profile = EmployeeBio.objects.get(user=cls.employee_user)
        cls.employee_profile.services.add(cls.service)
        cls.url = reverse('homepage')


    def setUp(self):
        self.client.login(username='client', password='asd123')
        self.url = reverse('appointment-create')
        self.future_date = (date.today() + timedelta(days=1)).isoformat()

    def test_get_request_renders_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)


    def test_post_valid_data_creates_appointment_and_redirects(self):
        post_data = {
            'employee': self.employee_profile.id,
            'service': self.service.id,
            'date': self.future_date,
            'start_time': '09:00',
            'comment': 'Test comment',
        }
        response = self.client.post(self.url, data=post_data)

        # redirect after successful form submission
        self.assertEqual(response.status_code, 302)

        appointment = Appointment.objects.first()
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.client, self.client_profile)
        self.assertEqual(appointment.employee, self.employee_profile)
        self.assertEqual(appointment.service, self.service)
        self.assertEqual(appointment.comment, 'Test comment')

    def test_post_invalid_data_returns_form_errors(self):
        # Missing service, which is required
        post_data = {
            'employee': self.employee_profile.id,
            'date': self.future_date,
            'start_time': '09:00',
        }

        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertIn('service', form.errors)
        self.assertIn('Моля, изберете услуга.', form.errors['service'])

    def test_initial_data_from_url_parameters(self):
        # Pass DATE and START_TIME in query string
        date_str = self.future_date
        start_time_str = '10:30'

        response = self.client.get(
            f"{self.url}?date={date_str}&start_time={start_time_str}"
        )
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertEqual(form.initial.get('date'), date_str)
        self.assertEqual(form.initial.get('start_time'), start_time_str)

    def test_login_required_redirects_anonymous(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
