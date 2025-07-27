from datetime import date, time, timedelta
from django.test import TestCase
from accounts.models import BaseUser, ClientProfile, EmployeeBio
from appointments.models import Appointment, DayOff
from appointments.utils import find_earliest_available_slots
from services.models import BaseService


class TestFindEarliestSlots(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_user = BaseUser.objects.create_user(username="client3", email='client3@mail.com', password="pass123", telephone_number='089712421346')
        cls.employee_user = BaseUser.objects.create_user(username="employee3", email='employee3@mail.com', password="pass123", telephone_number='08971332346')
        cls.client_profile = ClientProfile.objects.get_or_create(user=cls.client_user)[0]
        cls.employee = EmployeeBio.objects.get_or_create(user=cls.employee_user)[0]
        cls.service = BaseService.objects.create(name="Nails", duration=60, price=90)

    def test_earliest_available_slots__excludes_occupied_slots__no_day_off__date_is_present(self):
        target_date = date.today() + timedelta(days=1)

        Appointment.objects.create(
            client=self.client_profile,
            employee=self.employee,
            service=self.service,
            date=target_date,
            start_time=time(9, 0),
            created_by=self.client_user
        )

        slots = find_earliest_available_slots(
            employee=self.employee,
            service=self.service,
            start_date=target_date,
            MAX_SLOTS_PER_DAY=5
        )

        for slot in slots:
            self.assertNotEqual(slot["start_time"], time(9, 0))

    def test_earliest_available_slots___no_appointment__no_day_off__date_is_present(self):
        target_date = date.today() + timedelta(days=1)

        slots = find_earliest_available_slots(
            employee=self.employee,
            service=self.service,
            start_date=target_date,
            MAX_SLOTS_PER_DAY=5
        )

        self.assertEqual(len(slots), 5)
        self.assertEqual(slots[0]["employee"], self.employee)
        self.assertEqual(slots[0]["service"], self.service)

    def test_earliest_available_slots___no_appointment__with_day_off__date_is_present(self):
        # Skipping Day Off so there is no available slot for today
        target_date = date.today()


        day_off = DayOff(employee=self.employee, date=target_date)
        day_off.save()

        slots = find_earliest_available_slots(
            employee=self.employee,
            service=self.service,
            start_date=target_date,
            MAX_SLOTS_PER_DAY=5,
        )

        self.assertEqual(len(slots), 0)

    def test_earliest_available_slots___no_appointment__no_day_off__date_is_past(self):
        # The date is yesterday so there is no available present slots
        target_date = date.today() - timedelta(days=1)

        slots = find_earliest_available_slots(
            employee=self.employee,
            service=self.service,
            start_date=target_date,
            MAX_SLOTS_PER_DAY=5,
        )

        self.assertEqual(len(slots), 0)