from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.peoples.models import UserEmployee
from django_token.models import Token
import djclick as click


def is_log():

    token = UserEmployee().token_is_valid()
    if isinstance(token, Token):
        return token
    else:
        return click.secho(f"You need to be logged", fg="red")

