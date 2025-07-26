from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import date, timedelta
from appointments.forms import DayOffForm
from appointments.models import DayOff, Appointment
from accounts.models import EmployeeBio, BaseUser, ClientProfile
from services.models import BaseService


class DayOffFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.employee_user = BaseUser.objects.create_user(
            username='employee',
            email='employee@mail.com',
            password='asd123',
            telephone_number='0897122237'
        )

        cls.client_user = BaseUser.objects.create_user(
            username='client',
            email='client@mail.com',
            password='pass123',
            telephone_number='08971112346'
        )

        cls.client_profile = ClientProfile.objects.get_or_create(user=cls.client_user)[0]
        cls.employee = EmployeeBio.objects.get_or_create(user=cls.employee_user)[0]

        cls.service = BaseService.objects.create(name="Маникюр", price=50, duration=60)
        cls.employee.services.add(cls.service)

    def test_valid_day_off(self):
        tomorrow = date.today() + timedelta(days=1)
        form = DayOffForm(
            data={'date': tomorrow},
            employee=self.employee
        )

        self.assertTrue(form.is_valid())

        day_off = form.save(commit=False)
        day_off.employee = self.employee

        day_off.clean()
        day_off.save()

    def test_day_off_in_past_raises_validation_error(self):
        past_date = date.today() - timedelta(days=1)
        day_off = DayOff(
            employee=self.employee,
            date=past_date
        )

        with self.assertRaises(ValidationError) as cm:
            day_off.clean()
        self.assertIn('Не може да отбележиш ден като почивен в миналото.', cm.exception.message_dict['date'])

    def test_day_off_with_appointments_raises_validation_error(self):
        tomorrow = date.today() + timedelta(days=1)

        Appointment.objects.create(
            client=self.client_profile,
            employee=self.employee,
            service=self.service,
            date=tomorrow,
            start_time='10:00'
        )

        day_off = DayOff(
            employee=self.employee,
            date=tomorrow
        )

        with self.assertRaises(ValidationError) as cm:
            day_off.clean()
        self.assertIn('Не може да отбележиш ден като почивен, защото има записани клиенти.', cm.exception.message_dict['date'])

    def test_duplicate_day_off_raises_validation_error(self):
        tomorrow = date.today() + timedelta(days=1)

        DayOff.objects.create(
            employee=self.employee,
            date=tomorrow
        )

        day_off = DayOff(employee=self.employee, date=tomorrow)

        with self.assertRaises(ValidationError) as cm:
            day_off.clean()
        self.assertIn('Деня вече е отбелязан като почивен.', cm.exception.message_dict['date'])
