from datetime import date, timedelta, time
from django.core.exceptions import ValidationError
from django.test import TestCase
from accounts.models import ClientProfile, EmployeeBio, BaseUser
from appointments.models import Appointment
from appointments.config import WORK_START, WORK_END
from services.models import BaseService


class TestAppointmentValidations(TestCase):
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

        cls.client_profile = ClientProfile.objects.get_or_create(user=cls.client_user)[0]
        cls.employee = EmployeeBio.objects.get_or_create(user=cls.employee_user)[0]

        cls.service = BaseService.objects.create(name='test service', duration=120, price=100)

    def test_valid_appointment_creation(self):
        appointment = Appointment(
            client=self.client_profile,
            employee=self.employee,
            service=self.service,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            created_by=self.client_user,
        )
        appointment.full_clean()
        appointment.save()
        self.assertIsNotNone(appointment)

    def test_missing_employee_raises_value_error(self):
        appointment = Appointment(
            client=self.client_profile,
            employee=None,
            service=self.service,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            created_by=self.client_user,
        )
        with self.assertRaises(ValueError):
            appointment.save()

    def test_appointment_creation_with_past_date(self):
        appointment = Appointment(
            client=self.client_profile,
            employee=self.employee,
            service=self.service,
            date=date.today() - timedelta(days=1),
            start_time=time(10, 0),
            created_by=self.client_user,
        )
        with self.assertRaises(ValidationError) as e:
            appointment.full_clean()
        exc = e.exception
        self.assertIn('__all__', exc.message_dict)
        self.assertIn("Не може да се записва процедура за минала дата.", exc.message_dict['__all__'])

    def test_appointment_creation_when_the_studio_is_closed__early_hours(self):
        appointment = Appointment(
            client=self.client_profile,
            employee=self.employee,
            service=self.service,
            date=date.today() + timedelta(days=1),
            start_time=time(8, 0),
            created_by=self.client_user,
        )
        with self.assertRaises(ValidationError) as e:
            appointment.full_clean()
        exc = e.exception
        self.assertIn('__all__', exc.message_dict)
        self.assertIn(
            f"Процедурата трябва да е в рамките на работното време "
            f"({WORK_START.strftime('%H:%M')} - {WORK_END.strftime('%H:%M')}).",
            exc.message_dict['__all__']
        )


    def test_appointment_creation_when_the_studio_is_closed__late_hours(self):
        appointment = Appointment(
            client=self.client_profile,
            employee=self.employee,
            service=self.service,
            date=date.today() + timedelta(days=1),
            start_time=time(20, 0),
            created_by=self.client_user,
        )
        with self.assertRaises(ValidationError) as e:
            appointment.full_clean()

        exc = e.exception
        self.assertIn('__all__', exc.message_dict)
        self.assertIn(
            f"Процедурата трябва да е в рамките на работното време "
            f"({WORK_START.strftime('%H:%M')} - {WORK_END.strftime('%H:%M')}).",
            exc.message_dict['__all__']
        )

    def test_appointment_creation_when_the_procedure_overlaps_with_another_procedure(self):
        Appointment.objects.create(
            client=self.client_profile,
            employee=self.employee,
            service=self.service,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            created_by=self.client_user,
        )

        overlapping = Appointment(
            client=self.client_profile,
            employee=self.employee,
            service=self.service,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 20),
            created_by=self.client_user,
        )

        with self.assertRaises(ValidationError) as e:
            overlapping.full_clean()

        exc = e.exception
        self.assertIn('__all__', exc.message_dict)
        self.assertIn(
            "Това време е заето – процедурата започнала по-рано още не е приключила.",
            exc.message_dict['__all__']
        )
