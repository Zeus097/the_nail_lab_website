from services.models import BaseService
from accounts.models import EmployeeBio


def inject_service_if_valid(service_id, kwargs):
    service = BaseService.objects.filter(id=service_id).first()
    if service:
        kwargs['service'] = service
        kwargs.setdefault('initial', {})['service'] = service
    return kwargs


def inject_employee_if_valid(employee_id, kwargs):
    try:
        emp_id = int(str(employee_id).strip())  # ще хвърли ако е '' или None
    except (TypeError, ValueError):
        return kwargs  # нищо не добавяме

    employee = EmployeeBio.objects.filter(id=emp_id).first()
    if employee:
        kwargs.setdefault('initial', {})['employee'] = employee.id
    return kwargs
