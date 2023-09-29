import djclick as click
from django.core.management import BaseCommand

from apps.peoples.models import UserEmployee
from django.urls import path
from django_token.models import Token
import datetime


@click.command()
def logout():
    """
        Logout
    """

    user = UserEmployee()
    token = user.token_is_valid()

    if isinstance(token, Token):
        user.logout(token.user)
        click.secho(f"You are disconnected", fg="green")
    else:
        click.secho(f"You are not connected", fg="red")
