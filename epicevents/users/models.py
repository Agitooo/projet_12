from django.contrib.auth.models import User, AbstractUser
from django.db import models


class UserEmployee(models.Model):

    EMPLOYEE_COMMERCIAL = 1
    EMPLOYEE_SUPPORT = 2
    EMPLOYEE_GESTION = 3

    EMPLOYEE_DEPARTMENT = [
        (EMPLOYEE_COMMERCIAL, 'commercial'),
        (EMPLOYEE_SUPPORT, 'support'),
        (EMPLOYEE_GESTION, 'gestion')
    ]

    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    department = models.PositiveSmallIntegerField(choices=EMPLOYEE_DEPARTMENT)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)
    objects = models.Manager()

    class Meta:
        verbose_name = "employé"
        verbose_name_plural = "employés"

    def __str__(self):
        return self.employee.name


class UserClient(models.Model):

    client = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    company = models.CharField(max_length=256)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)
    contact = models.ForeignKey(UserEmployee, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        verbose_name = "client"
        verbose_name_plural = "clients"

    def __str__(self):
        return self.client.name
