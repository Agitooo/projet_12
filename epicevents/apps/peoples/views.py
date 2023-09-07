from django.shortcuts import render
from .permissions import CreateEmployeePermissions, ReadEmployeePermissions, \
    UpdateEmployeePermissions, DeleteEmployeePermissions, \
    CreateCustomerPermissions, ReadCustomerPermissions, UpdateCustomerPermissions


# createEmployee
#     permission_classes = [CreateEmployeePermissions]

# getAllEmployee
#     permission_classes = [ReadEmployeePermissions]

# getEmployee
#     permission_classes = [ReadEmployeePermissions]

# updateEmployee
#     permission_classes = [UpdateEmployeePermissions]

# deleteEmployee
#     permission_classes = [DeleteEmployeePermissions]


# createClient
#     permission_classes = [CreateCustomerPermissions]

# getAllClients
#     permission_classes = [ReadCustomerPermissions]

# getClient
#     permission_classes = [ReadCustomerPermissions]

# updateClient
#     permission_classes = [UpdateCustomerPermissions]
