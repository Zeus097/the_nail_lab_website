from datetime import datetime, timedelta
from appointments.models import Appointment, DayOff
from appointments.config import WORK_START, WORK_END, INTERVAL, DAYS_AHEAD


def find_earliest_available_slots(employee, service, start_date, max_slots=5):
    slots = []
    duration = timedelta(minutes=service.duration)
    date = start_date

    for day in range(DAYS_AHEAD):
        current_date = date + timedelta(days=day)

        if DayOff.objects.filter(employee=employee, date=current_date).exists():
            continue

        appointments = Appointment.objects.filter(employee=employee, date=current_date)
        start_dt = datetime.combine(current_date, WORK_START)
        end_dt = datetime.combine(current_date, WORK_END) - duration

        while start_dt <= end_dt:
            slot_start = start_dt
            slot_end = slot_start + duration

            overlaps = False
            for appt in appointments:
                appt_start = datetime.combine(appt.date, appt.start_time)
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

            if len(slots) >= max_slots:
                return slots

            start_dt += INTERVAL

    return slots
