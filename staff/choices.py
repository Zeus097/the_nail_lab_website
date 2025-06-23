from django.db.models import TextChoices


class JobTypeChoice(TextChoices):
    NAILS = "nl", "МАНИКЮРИСТ"
    MAKEUP = "mkp", "ГРИМЬОР"
    HAIRCUT = "hct", "ФРИЗЬОР"
