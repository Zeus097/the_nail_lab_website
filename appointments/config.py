from datetime import date, time, timedelta

WORK_START = time(9, 0)
WORK_END = time(20, 0)
INTERVAL = timedelta(minutes=15)
DAYS_AHEAD = 1


def is_sunday(d: date) -> bool:
    return d.weekday() == 6


# Work day max slots if employee has a free schedule
MAX_SLOTS_PER_DAY = 36
