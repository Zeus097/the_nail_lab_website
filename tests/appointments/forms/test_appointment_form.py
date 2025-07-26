from django.test import TestCase
from datetime import date, time, timedelta
from appointments.forms import AppointmentForm
from accounts.models import EmployeeBio, BaseUser, ClientProfile
from services.models import BaseService


class AppointmentFormTest(TestCase):
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
            password='pass',
            telephone_number='0897122237'
        )

        cls.employee_user2 = BaseUser.objects.create_user(
            username='employee2',
            email='employee2@mail.com',
            password='pass321',
            telephone_number='0897333237'
        )

        cls.client_profile = ClientProfile.objects.get_or_create(user=cls.client_user)[0]
        cls.employee = EmployeeBio.objects.get_or_create(user=cls.employee_user)[0]
        cls.employee2 = EmployeeBio.objects.get_or_create(user=cls.employee_user2)[0]

        cls.service1 = BaseService.objects.create(name="Маникюр", price=50, duration=60)
        cls.service2 = BaseService.objects.create(name="Педикюр", price=60, duration=45)

        cls.employee.services.add(cls.service1)
        cls.employee2.services.add(cls.service2)

    def test_valid_form_with_all_required_fields(self):
        # Use tomorrow's date to avoid past date errors
        tomorrow = date.today() + timedelta(days=1)

        # Fixed time in order for the test to pass the past time or closed studio error
        fixed_time = time(10, 0)

        form_data = {
            "employee": self.employee.pk,
            "service": self.service1.pk,
            "date": tomorrow,
            "start_time": fixed_time,
        }

        form = AppointmentForm(data=form_data, employee_id=self.employee.pk)
        self.assertTrue(form.is_valid())

    def test_missing_service_triggers_clean_error(self):
        tomorrow = date.today() + timedelta(days=1)
        fixed_time = time(10, 0)

        form_data = {
            "employee": self.employee.pk,
            "service": '',
            "date": tomorrow,
            "start_time": fixed_time,
        }

        form = AppointmentForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("service", form.errors)
        self.assertEqual(form.errors["service"], ["Това поле е задължително.", "Моля, изберете услуга."])

    def test_service_queryset_filtered_by_employee_id(self):

        # employee2 only has service2
        form_for_employee2 = AppointmentForm(employee_id=self.employee2.pk)
        service_ids_employee2 = [s.id for s in form_for_employee2.service_queryset]

        self.assertIn(self.service2.id, service_ids_employee2)
        self.assertNotIn(self.service1.id, service_ids_employee2)

        # same with employee1
        form_for_employee1 = AppointmentForm(employee_id=self.employee.pk)
        service_ids_employee1 = [s.id for s in form_for_employee1.service_queryset]

        self.assertIn(self.service1.id, service_ids_employee1)
        self.assertNotIn(self.service2.id, service_ids_employee1)
