from datetime import date, timedelta, time
from django.core.exceptions import ValidationError
from django.test import TestCase
from accounts.models import ClientProfile, EmployeeBio, BaseUser
from services.models import BaseService
from appointments.models import DayOff, Appointment

class TestDayOffValidation(TestCase):
    @classmethod
    def setUpTestData(cls):
        client_user = BaseUser.objects.create_user(username='client', email='client@mail.com', password='pass123', telephone_number='08971212346')
        employee_1_user = BaseUser.objects.create_user(username='employee1', email='empl1@mail.com', password='pass345', telephone_number='08972212346')
        employee_2_user = BaseUser.objects.create_user(username='employee2', email='empl2@mail.com', password='pass567', telephone_number='08973312346')

        cls.client_profile = ClientProfile.objects.get_or_create(user=client_user)[0]
        cls.employee = EmployeeBio.objects.get_or_create(user=employee_1_user)[0]
        cls.employee_2 = EmployeeBio.objects.get_or_create(user=employee_2_user)[0]
        cls.service = BaseService.objects.create(name='test', duration=120, price=100)
        cls.rest_day_today = date.today()

    def test_day_off___same_employees_same_day_case(self):
        DayOff.objects.create(employee=self.employee, date=self.rest_day_today)

        with self.assertRaises(ValidationError) as e:
            DayOff(employee=self.employee, date=self.rest_day_today).full_clean()
        self.assertIn("Деня вече е отбелязан като почивен.", e.exception.message_dict['date'])

    def test_day_off__different_employees_same_day(self):
        DayOff.objects.create(employee=self.employee, date=self.rest_day_today)
        DayOff.objects.create(employee=self.employee_2, date=self.rest_day_today)

        self.assertEqual(
            DayOff.objects.filter(date=self.rest_day_today).count(), 2
        )

    def test_day_off___past_date_case(self):
        day_off = DayOff(employee=self.employee, date=self.rest_day_today - timedelta(days=2))
        # Checks with 2 days because after midnight sometimes checks still previous day

        with self.assertRaises(ValidationError) as e:
            day_off.full_clean()
        self.assertIn("Не може да отбележиш ден като почивен в миналото.", e.exception.message_dict['date'])

    def test_day_off___valid_appointment_same_day_case(self):
        Appointment.objects.create(
            client=self.client_profile,
            employee=self.employee,
            service=self.service,
            date=self.rest_day_today,
            start_time=time(10, 0),
            created_by=self.client_profile.user,
        )

        day_off = DayOff(employee=self.employee, date=self.rest_day_today)

        with self.assertRaises(ValidationError) as e:
            day_off.full_clean()
        self.assertIn("Не може да отбележиш ден като почивен, защото има записани клиенти.", e.exception.message_dict['date'])

    def test_appointment_creation_when_the_day_is_marked_as_rest_day(self):
        DayOff(employee=self.employee, date=self.rest_day_today).save()

        appointment = Appointment(
            client=self.client_profile,
            employee=self.employee,
            service=self.service,
            date=self.rest_day_today,
            start_time=time(10, 0),
            created_by=self.client_profile.user,
        )

        with self.assertRaises(ValidationError) as e:
            appointment.full_clean()

        self.assertIn(
            "Денят е отбелязан като почивен.",
            str(e.exception)
            )
