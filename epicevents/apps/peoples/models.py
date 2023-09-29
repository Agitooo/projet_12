from django.contrib.auth.models import AbstractUser, Group
from django.db import models
import os
import datetime

from settings.settings import EMPLOYEE_LOGIN_DURATION_VALIDITY
from django.contrib.auth import authenticate
from django_token.models import Token


class UserEmployee(AbstractUser):

    PERMISSION_EMPLOYEE_NAME = 'employé'

    EMPLOYEE_COMMERCIAL = 1
    EMPLOYEE_SUPPORT = 2
    EMPLOYEE_GESTION = 3

    EMPLOYEE_GROUPE_SUPPORT = 1
    EMPLOYEE_GROUPE_COMMERCIAL = 2
    EMPLOYEE_GROUPE_GESTION = 3

    EMPLOYEE_DEPARTMENT = [
        (EMPLOYEE_COMMERCIAL, 'Commercial'),
        (EMPLOYEE_SUPPORT, 'Support'),
        (EMPLOYEE_GESTION, 'Gestion')
    ]

    phone = models.CharField(max_length=10)
    department = models.PositiveSmallIntegerField(choices=EMPLOYEE_DEPARTMENT, default=EMPLOYEE_GESTION)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    # objects = models.Manager()

    class Meta:
        verbose_name = "employé"
        verbose_name_plural = "employés"

    def __str__(self):
        return self.username

    def logout(self, user):
        try:
            # Si on a un token on le supprime
            Token.objects.filter(user=user).delete()
            self.delete_token_file()
            return True
        except Token.DoesNotExist:
            self.delete_token_file()
            return True

    def get_group_by_dpt(self, dpt_id):
        match dpt_id:
            case self.EMPLOYEE_COMMERCIAL:
                return self.EMPLOYEE_GROUPE_COMMERCIAL
            case self.EMPLOYEE_SUPPORT:
                return self.EMPLOYEE_GROUPE_SUPPORT
            case self.EMPLOYEE_GESTION:
                return self.EMPLOYEE_GROUPE_GESTION
            case _:
                return None

    def create_user(self, username, password, email, lastname, firstname, phone, dpt_id):
        try:
            user = UserEmployee.objects.create_user(username, email, password)
            user.last_name = lastname
            user.first_name = firstname
            user.phone = phone
            user.department = dpt_id

            # On récupère le groupe qui correspond au département saisi
            group_id = self.get_group_by_dpt(dpt_id)
            group = Group.objects.get(id=group_id)

            # Ajout le groupe sur le user
            user.groups.add(group)
            user.save()

            return user

        except TypeError:
            return 'invalid type'

    def authenticate_user(self, username, password):
        return authenticate(username=username, password=password)

    def set_token(self, user):
        try:
            # Si on a deja un token et qu'on se log, on supprime l'existant
            Token.objects.filter(user=user).delete()
            self.delete_token_file()
            # et on en génère un nouveau EN DB et en local
            token = Token.objects.create(user=user)
            self.save_token_file(token)
            return token
        except Token.DoesNotExist:
            # Si le token n'existe pas ou moment de se logger, on en créé un
            token = Token.objects.create(user=user)
            self.save_token_file(token)
            return token

    def save_token_file(self, token):
        with open('login/token', 'a') as login:
            login.write(token.key)

    def load_token_file(self):
        if os.path.isfile("login/token"):
            with open('login/token', 'r') as login:
                token = login.read()
                return token
        else:
            return None

    def delete_token_file(self):
        if os.path.isfile("login/token"):
            os.remove("login/token")

    def token_is_valid(self):
        try:
            # On récupère le token.key du fichier local
            token_key_load = self.load_token_file()
            if token_key_load:
                # On regarde si on a bien un token qui correspond a la key en local
                token = Token.objects.get(key=token_key_load)
                # S'il y a un token
                if token and token.key == token_key_load:
                    token_created = int(round(token.created.timestamp()))
                    now = int(round(datetime.datetime.now().timestamp()))
                    # On regarde qu'il a été créé il y a moins de
                    # 'EMPLOYEE_LOGIN_DURATION_VALIDITY' secondes
                    if token_created <= now <= (token_created + EMPLOYEE_LOGIN_DURATION_VALIDITY):
                        return token
                    else:
                        # Sinon on supprime le token et on doit se logger
                        Token.objects.filter(user=token.user).delete()
                        self.delete_token_file()
                        return False
                else:
                    return False
            else:
                return False
        except Token.DoesNotExist:
            return False

    def has_permission(self, user, permission_to_check):
        user_groups = user.groups.all()
        for group in user_groups:
            permissions = group.permissions.all()
            for permission in permissions:
                if permission.name == permission_to_check:
                    return True
        return False


class Customer(models.Model):

    PERMISSION_CUSTOMER_NAME = 'client'

    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    company = models.CharField(max_length=256)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)
    created_by = models.ForeignKey(UserEmployee, on_delete=models.CASCADE, related_name="created_by")
    contact = models.ForeignKey(
        UserEmployee,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="commercial_contact"
    )
    objects = models.Manager()

    class Meta:
        verbose_name = "client"
        verbose_name_plural = "clients"

    def __str__(self):
        return f"{self.lastname} {self.firstname}"
