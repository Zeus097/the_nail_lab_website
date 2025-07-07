from django.contrib.auth import login

from accounts.models import ClientProfile


def create_client_profile(backend, user, response, *args, **kwargs):
    # Създаване на клиентски профил, ако липсва
    if not hasattr(user, 'clientprofile'):
        ClientProfile.objects.create(user=user)

    # Ако потребителят няма usable парола – задаваме невалидна парола
    if not user.has_usable_password():
        user.set_unusable_password()
        user.save()


def check_profile_data(strategy, details, user=None, *args, **kwargs):
    if not user:
        return

    # Проверяваме дали има ClientProfile (ако липсва, няма смисъл да продължаваме)
    if not hasattr(user, 'clientprofile'):
        return

    # Проверка за парола и телефон (на user)
    if not user.has_usable_password() or not user.telephone_number:
        login(strategy.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return strategy.redirect('/accounts/complete-profile/')



