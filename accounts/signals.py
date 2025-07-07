from accounts.models import ClientProfile, EmployeeBio

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def sync_user_profiles(sender, instance, created, **kwargs):

    # NEW USER
    if created:
        if not instance.is_employee:
            instance.is_client = True
            instance.save(update_fields=['is_client'])

    # PROFILE FOR EMPLOYEES
    if instance.is_employee:
        try:
            profile = instance.employeebio
            if profile.name != instance.username:
                profile.name = instance.username
                profile.save()
        except EmployeeBio.DoesNotExist:
            EmployeeBio.objects.create(user=instance, name=instance.username)

    # PROFILE FOR CLIENTS
    if instance.is_client:
        try:
            _ = instance.clientprofile
            # _ because the object variable is not important(won't use in other places),
            # but to check if it exists!

        except ClientProfile.DoesNotExist:
            ClientProfile.objects.create(user=instance)
