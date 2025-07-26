from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from appointments.models import Appointment

from accounts.models import ClientProfile, EmployeeBio, BaseUser

from services.models import BaseService

from datetime import date, time

User = get_user_model()


class TestAppointmentDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_user = BaseUser.objects.create_user(
            username='client',
            email='client@mail.com',
            password='pass123',
            telephone_number='08971112346'
        )

        cls.employee_user = BaseUser.objects.create_user(
            username='employee',
            email='employee@mail.com',
            password='asd321386',
            telephone_number='0897122237'
        )

        cls.client_profile = ClientProfile.objects.get_or_create(user=cls.client_user)[0]
        cls.employee_profile = EmployeeBio.objects.get_or_create(user=cls.employee_user)[0]

        cls.service = BaseService.objects.create(name='test service', duration=120, price=100)


    def setUp(self):
        self.appointment = Appointment.objects.create(
            client=self.client_profile,
            employee=self.employee_profile,
            service=self.service,
            date=date.today(),
            start_time=time(10, 0),
        )

        self.url = reverse('appointment-delete', kwargs={'pk': self.appointment.pk})

    def test_owner_can_delete_appointment(self):
        self.client.login(username='client', password='pass123')
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('homepage'))
        self.assertFalse(Appointment.objects.filter(pk=self.appointment.pk).exists())

    def test_non_owner_cannot_delete_appointment(self):
        self.client.login(username='employee', password='asd321386')
        response = self.client.post(self.url)

        # Redirect to homepage due to handle_no_permission
        self.assertRedirects(response, reverse('homepage'))
        self.assertTrue(Appointment.objects.filter(pk=self.appointment.pk).exists())

    def test_get_request_renders_confirmation_template(self):
        self.client.login(username='client', password='pass123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/appointment_delete_confirmation.html')
        self.assertContains(response, 'Сигурни ли сте?')
