from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from accounts.models import ClientProfile, EmployeeBio
from services.models import BaseService
from appointments.models import Appointment

User = get_user_model()


class CurrentAppointmentEditViewTests(TestCase):
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
            password='pass5678',
            email='employee@example.com',
            is_employee=True,
        )

        cls.service1 = BaseService.objects.create(
            name='Ноктопластика',
            price=100,
            duration=90,
        )

        cls.service2 = BaseService.objects.create(
            name='Manicure',
            price=60,
            duration=60,
        )

        cls.employee_profile = EmployeeBio.objects.get(
            user=cls.employee_user
        )
        cls.employee_profile.services.set(
            [
                cls.service1,
                cls.service2
            ]
        )

        cls.client_profile = ClientProfile.objects.get(
            user=cls.client_user
        )

        cls.appointment = Appointment.objects.create(
            client=cls.client_profile,
            employee=cls.employee_profile,
            service=cls.service1,
            date=timezone.localdate() + timezone.timedelta(days=1),
            start_time=timezone.datetime.strptime('10:00', '%H:%M').time(),
            comment='Тест'
        )

        cls.url = reverse('appointment-edit', kwargs={'pk': cls.appointment.pk})

    def setUp(self):
        self.client.login(username='client', password='asd123')
        self.future_date = (date.today() + timedelta(days=1)).isoformat()

    def test_post_valid_data_updates_appointment_and_redirects(self):
        post_data = {
            'employee': self.employee_profile.id,
            'service': self.service2.id,
            'date': self.future_date,
            'start_time': '11:30',
            'comment': 'Нов тест',
        }

        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 302)

        self.appointment.refresh_from_db()

        self.assertEqual(self.appointment.comment, 'Нов тест')
        self.assertEqual(self.appointment.service, self.service2)
        self.assertEqual(self.appointment.start_time.strftime('%H:%M'), '11:30')

    def test_post__invalid_empty_data__returns_form_with_errors(self):
        post_data = {
            'employee': self.employee_profile.id,
            'service': '',
            'date': '',
            'start_time': '',
        }

        response = self.client.post(self.url, data=post_data)
        response.render()

        form = response.context['form']
        self.assertTrue(form.errors)

        self.assertIn('service', form.errors)
        self.assertIn('Моля, изберете услуга.', form.errors['service'])

        self.assertIn('date', form.errors)
        self.assertIn('Това поле е задължително.', form.errors['date'])
