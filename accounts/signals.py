from django.contrib.auth import get_user_model

from django.db.models.signals import post_save, pre_save

from django.dispatch import receiver

from accounts.models import ClientProfile, EmployeeBio, BaseUser


import cloudinary.uploader



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



# signal for deleting old profile picture in Cloudinary, after changing

@receiver(pre_save, sender=BaseUser)
def delete_old_photo_if_changed(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = BaseUser.objects.get(pk=instance.pk)
    except BaseUser.DoesNotExist:
        return

    old_photo = old_instance.photo
    new_photo = instance.photo


    if old_photo and old_photo != new_photo:
        try:
            public_id = old_photo.name.rsplit('.', 1)[0]
            cloudinary.uploader.destroy(public_id)
        except Exception as e:
            print(f"Cloudinary deletion error: {e}")
