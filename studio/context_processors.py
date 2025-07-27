def user_role_context(request):
    # Used in settings.py in TEMPLATES

    user = request.user
    is_employee = user.is_authenticated and user.is_employee
    return {'is_employee': is_employee}
