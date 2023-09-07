from rest_framework.permissions import BasePermission
from apps.peoples.models import Customer, UserEmployee
from apps.contracts.models import Contract
from apps.events.models import Event


class CreateEventPermissions(BasePermission):
    def has_permission(self, request, view):
        customer_pk = view.kwargs['customer_pk']
        customer = Customer.objects.get(pk=customer_pk)
        customers = Customer.objects.filter(commercial_contact__user=request.user)
        if customer in customers and request.user.department == UserEmployee.EMPLOYEE_COMMERCIAL:
            return True
        else:
            return False
    # seulement Commercial (ses clients si contrat signé)


class ReadEventPermissions(BasePermission):
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


class UpdateEventPermissions(BasePermission):
    def has_permission(self, request, view):
        event_pk = view.kwargs['event_pk']
        event = Event.objects.get(pk=event_pk)
        events = Event.objects.filter(support_contact__user=request.user)
        if \
                request.user.department == UserEmployee.EMPLOYEE_GESTION \
                or \
                (event in events and request.user.department == UserEmployee.EMPLOYEE_SUPPORT):
            return True
        else:
            return False
    # Gestion (associe un support a l'évent) / Support (ses events)
