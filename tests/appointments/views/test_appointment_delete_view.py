from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

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

        # Mocking
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
            name='test service',
            duration=120,
            price=100,
        )
        cls.service.service_photo.save('small.gif', image, save=True)

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
