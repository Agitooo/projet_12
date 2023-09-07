from rest_framework.permissions import BasePermission
from apps.peoples.models import Customer, UserEmployee
from apps.contracts.models import Contract


class CreateContractPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == UserEmployee.EMPLOYEE_GESTION:
            return True
        else:
            return False
    # seulement Gestion créé contrat et associe au client


class ReadContractPermissions(BasePermission):
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


class UpdateContractPermissions(BasePermission):
    def has_permission(self, request, view):
        customer_pk = view.kwargs['customer_pk']
        customer = Customer.objects.get(pk=customer_pk)
        customers = Customer.objects.filter(commercial_contact__user=request.user)
        if \
                request.user.department == UserEmployee.EMPLOYEE_GESTION \
                or \
                (request.user.department == UserEmployee.EMPLOYEE_COMMERCIAL and customer in customers):
            return True
        else:
            return False
    # Gestion / Commercial (ses clients => contrat signé)

