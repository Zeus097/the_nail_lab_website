from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import ClientProfile, EmployeeBio

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def sync_user_profiles(sender, instance, created, **kwargs):

    if created and not instance.is_employee:
        if not instance.is_client:
            instance.is_client = True
            instance.save(update_fields=['is_client'])

    if instance.is_employee:
        profile, created_bio = EmployeeBio.objects.get_or_create(
            user=instance,
            defaults={'name': instance.username}
        )
        if not created_bio and profile.name != instance.username:
            profile.name = instance.username
            profile.save(update_fields=['name'])

    if instance.is_client:
        ClientProfile.objects.get_or_create(user=instance)
