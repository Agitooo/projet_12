from rest_framework.permissions import BasePermission
from apps.peoples.models import Customer, UserEmployee


class CreateEmployeePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == UserEmployee.EMPLOYEE_GESTION:
            return True
        else:
            return False


class ReadEmployeePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == UserEmployee.EMPLOYEE_GESTION:
            return True
        else:
            return False


class UpdateEmployeePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == UserEmployee.EMPLOYEE_GESTION:
            return True
        else:
            return False


class DeleteEmployeePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == UserEmployee.EMPLOYEE_GESTION:
            return True
        else:
            return False


class CreateCustomerPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == UserEmployee.EMPLOYEE_COMMERCIAL:
            return True
        else:
            return False


class ReadCustomerPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.department in (
                UserEmployee.EMPLOYEE_COMMERCIAL,
                UserEmployee.EMPLOYEE_GESTION,
                UserEmployee.EMPLOYEE_SUPPORT
        ):
            return True
        else:
            return False
    # Gestion / support / commercial


class UpdateCustomerPermissions(BasePermission):
    def has_permission(self, request, view):
        customer_pk = view.kwargs['customer_pk']
        customer = Customer.objects.get(pk=customer_pk)
        customers = Customer.objects.filter(commercial_contact__user=request.user)
        if customer in customers:
            return True
        else:
            return False
    # seulement Commercial associé
