from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.timezone import localtime, localdate
from appointments.config import WORK_START, WORK_END, is_sunday


@deconstructible
class AppointmentModelCleanValidator:
    def __init__(self, get_overlapping_qs=None, get_day_off_qs=None):
        self.get_overlapping_qs = get_overlapping_qs
        self.get_day_off_qs = get_day_off_qs

    def __call__(self, instance):
        if not all([instance.employee, instance.service, instance.date, instance.start_time]):
            return

        if instance.date < localdate():
            raise ValidationError("Не може да се записва процедура за минала дата.")

        end_time = instance.end_time
        if end_time is None:
            return

        if instance.start_time < WORK_START or end_time > WORK_END:
            raise ValidationError(
                f"Процедурата трябва да е в рамките на работното време "
                f"({WORK_START.strftime('%H:%M')} - {WORK_END.strftime('%H:%M')})."
            )

        appointment_start = datetime.combine(instance.date, instance.start_time)
        appointment_end = datetime.combine(instance.date, end_time)

        overlapping_qs = self.get_overlapping_qs(instance) if self.get_overlapping_qs else self._default_overlapping(instance)
        for other in overlapping_qs:
            other_start = datetime.combine(other.date, other.start_time)
            other_end = datetime.combine(other.date, other.end_time)
            if not (appointment_end <= other_start or appointment_start >= other_end):
                raise ValidationError("Това време е заето – процедурата започнала по-рано още не е приключила.")

        day_off_qs = self.get_day_off_qs(instance) if self.get_day_off_qs else self._default_day_off(instance)
        if day_off_qs.exists() or is_sunday(instance.date):
            raise ValidationError("Денят е отбелязан като почивен.")

        if instance.date == localdate():
            current_time = localtime().time()
            if instance.start_time < current_time:
                raise ValidationError("Не може да се запазва час за изминал час от днешния ден.")

    @staticmethod
    def _default_overlapping(instance):
        from appointments.models import Appointment  # lazy import to avoid circular dependency
        return Appointment.objects.filter(
            employee=instance.employee,
            date=instance.date
        ).exclude(pk=instance.pk)

    @staticmethod
    def _default_day_off(instance):
        from appointments.models import DayOff # same lazy import to avoid circular dependency as above
        return DayOff.objects.filter(
            employee=instance.employee,
            date=instance.date
        )
