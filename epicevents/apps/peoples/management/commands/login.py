import djclick as click
from django.core.management import BaseCommand

from apps.peoples.models import UserEmployee
from django.urls import path
from django_token.models import Token
import datetime


@click.command()
@click.option('--username', '-un', prompt=True)
@click.option('--password', '-pw', prompt=True, hide_input=True)
def login(username, password):
    """
        Loggin
    """
    try:
        user: UserEmployee = UserEmployee.objects.get(username=username)

        if user.check_password(password):
            current_user = user.authenticate_user(username, password)
            is_auth = user.is_authenticated
            if is_auth:
                # Création du token (en DB et dans un fichier local)
                user.set_token(user=current_user)
                click.secho(f"Welcome {username}", fg="green")
            else:
                click.secho(f"Invalid credential", fg="red")
        else:
            click.secho(f"Invalid credential", fg="red")
    except UserEmployee.DoesNotExist:
        click.secho(f"Connection refused", fg="red")
