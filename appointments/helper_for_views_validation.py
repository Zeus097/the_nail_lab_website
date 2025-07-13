from services.models import BaseService
from accounts.models import EmployeeBio


def inject_service_if_valid(service_id, kwargs):
    service = BaseService.objects.filter(id=service_id).first()
    if service:
        kwargs['service'] = service
        kwargs.setdefault('initial', {})['service'] = service
    return kwargs


def inject_employee_if_valid(employee_id, kwargs):
    employee = EmployeeBio.objects.filter(id=employee_id).first()
    if employee:
        kwargs.setdefault('initial', {})['employee'] = employee
    return kwargs
