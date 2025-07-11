from django.contrib.auth import login

from accounts.models import ClientProfile


def create_client_profile(backend, user, response, *args, **kwargs):
    if not hasattr(user, 'clientprofile'):
        ClientProfile.objects.create(user=user)

    # If user don't have usable password
    if not user.has_usable_password():
        user.set_unusable_password()
        user.save()


def check_profile_data(strategy, details, user=None, *args, **kwargs):
    if not user:
        return

    needs_completion = not user.has_usable_password() or not user.telephone_number

    if needs_completion:
        login(strategy.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return strategy.redirect('/accounts/complete-profile/')




