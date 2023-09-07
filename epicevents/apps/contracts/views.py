from django.shortcuts import render
# from django.contrib.auth.mixins import PermissionRequiredMixin
from .permissions import CreateContractPermissions, ReadContractPermissions, UpdateContractPermissions


# createContract
#     permission_classes = [CreateContractPermissions]

# getAllContracts
#     permission_classes = [ReadContractPermissions]

# getContract
#     permission_classes = [ReadContractPermissions]

# getContractNotTotallyPaid
#     permission_classes = [ReadContractPermissions]

# getContractNotSigned
#     permission_classes = [ReadContractPermissions]

# updateContract
#     permission_classes = [UpdateContractPermissions]
