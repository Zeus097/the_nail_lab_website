from datetime import datetime, timedelta
from math import ceil

from django.utils.timezone import localtime, make_aware
from appointments.models import Appointment, DayOff
from appointments.config import WORK_START, WORK_END, INTERVAL, DAYS_AHEAD


def aware_datetime(date_obj, time_obj):
    naive = datetime.combine(date_obj, time_obj)
    return make_aware(naive)
    #  TO PREVENT TYPE ERROR WHEN
    #  COMPARING timezone(offset-aware) WITH DIFFERENT OBJECT (offset-naive)
    #       - different object types


def find_earliest_available_slots(employee, service, start_date, MAX_SLOTS_PER_DAY):
    slots = []
    duration = timedelta(minutes=service.duration)
    today = localtime().date()
    now_time = localtime().time()

    if start_date < today:
        return []

    for day in range(DAYS_AHEAD):
        current_date = start_date + timedelta(days=day)

        if DayOff.objects.filter(employee=employee, date=current_date).exists():
            continue

        if current_date < today:
            continue

        appointments = Appointment.objects.filter(employee=employee, date=current_date)
        start_dt = aware_datetime(current_date, WORK_START)

        if current_date == today and now_time > WORK_START:
            current_dt = localtime()
            minute = ceil(current_dt.minute / (INTERVAL.seconds // 60)) * (INTERVAL.seconds // 60)
            rounded = current_dt.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=minute)
            start_dt = rounded

        end_dt = aware_datetime(current_date, WORK_END) - duration

        while start_dt <= end_dt:
            slot_start = start_dt
            slot_end = slot_start + duration

            overlaps = False
            for appt in appointments:
                appt_start = aware_datetime(appt.date, appt.start_time)
                appt_end = appt_start + timedelta(minutes=appt.service.duration)

                if not (slot_end <= appt_start or slot_start >= appt_end):
                    overlaps = True
                    break

            if not overlaps:
                slots.append({
                    "date": current_date,
                    "start_time": slot_start.time(),
                    "employee": employee,
                    "service": service,
                })

            if len(slots) >= MAX_SLOTS_PER_DAY:
                return slots

            start_dt += INTERVAL

    return slots
