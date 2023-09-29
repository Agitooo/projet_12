import djclick as click
from django.core.management import BaseCommand

from apps.peoples.models import UserEmployee
from django.urls import path
from django_token.models import Token
import datetime


@click.command()
def test_sentry():
    """
        Test Sentry
    """

    try:
        zero_division = 1/0
    except ZeroDivisionError:
        click.secho(f"You can not divise by 0", fg="red")
