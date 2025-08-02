from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import EmployeeBio, ClientProfile
from appointments.models import Appointment
from services.models import BaseService

User = get_user_model()

class TestHomePageView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('homepage')

        # Get Ready template to mock an image (GIF) for the tests to run
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
            name='test_service',
            duration=120,
            price=100,
        )

        # uploading the image
        cls.service.service_photo.save('small.gif', image, save=True)

        cls.client_user = User.objects.create_user(
            username='client',
            email='client@mail.com',
            password='123asd',
            is_client=True,
            telephone_number='0897112346',
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

        response = self.client.get(self.url)
        context = response.context

        self.assertIn('appointment_list', context)
        self.assertEqual(len(context['appointment_list']), 1)
        self.assertTrue(response.wsgi_request.user.is_client)


    def test_employee_gets_their_appointments(self):
        self.client.login(username='employee', password='asd123')

        Appointment.objects.create(
            employee=self.employee_profile,
            client=self.client_profile,
            date=date.today(),
            start_time='11:00',
            service=self.service,
        )

        response = self.client.get(self.url)
        context = response.context

        self.assertIn('is_employee', context)
        self.assertIn('is_admin', context)
        self.assertIn('appointment_list', context)
        self.assertTrue(context.get('is_employee'))
        self.assertTrue(response.wsgi_request.user.is_employee)



    def test_admin__context_view_case(self):
        self.client.login(username='admin', password='asd123534dgd')

        Appointment.objects.create(
            employee=self.employee_profile,
            client=self.client_profile,
            date=date.today(),
            start_time='11:00',
            service=self.service,
        )

        response = self.client.get(self.url)
        context = response.context


        self.assertIn('appointment_list', context)
        self.assertTrue(context.get('is_admin'))
        self.assertTrue(response.wsgi_request.user.is_superuser)
