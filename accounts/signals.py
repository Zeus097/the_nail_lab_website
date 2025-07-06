from accounts.models import ClientProfile, EmployeeBio

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def sync_user_profiles(sender, instance, created, **kwargs):
    if created:
        if instance.is_employee and not hasattr(instance, 'employeebio'):
            EmployeeBio.objects.create(user=instance, name=instance.username)
        if instance.is_client and not hasattr(instance, 'clientprofile'):
            ClientProfile.objects.create(user=instance)
    else:
        if instance.is_employee:
            try:
                profile = instance.employeebio
                if profile.name != instance.username:
                    profile.name = instance.username
                    profile.save()
            except EmployeeBio.DoesNotExist:
                EmployeeBio.objects.create(user=instance, name=instance.username)
        if instance.is_client:
            try:
                profile = instance.clientprofile
                profile.save()
            except ClientProfile.DoesNotExist:
                ClientProfile.objects.create(user=instance)