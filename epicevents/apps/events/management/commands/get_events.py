import djclick as click
from django.core.management import BaseCommand
from rich.console import Console
from rich.table import Table

from apps.peoples.models import UserEmployee
from apps.events.models import Event
from django_token.models import Token
from settings.settings import VIEW

console = Console()


@click.command()
def get_events():
    """
        Show all events
    """

    user = UserEmployee()
    token = user.token_is_valid()

    if isinstance(token, Token):

        is_allowed = user.has_permission(token.user, VIEW + Event.PERMISSION_EVENT_NAME)

        if is_allowed:

            table = Table(show_header=True)
            table.add_column("Event ID")
            table.add_column("Location")
            table.add_column("date_start")
            table.add_column("date_end")
            table.add_column("total_people")
            table.add_column("comment")
            table.add_column("Contract ID")
            table.add_column("Customer ID")
            table.add_column("Customer Firstname")
            table.add_column("Customer Lastname")
            events = Event.objects.filter(active=True)
            for event in events:
                table.add_row(
                    str(event.pk),
                    event.location, event.date_start, event.date_end, str(event.total_people), event.comment,
                    str(event.contract.pk),
                    str(event.contract.client.pk), event.contract.client.firstname, event.contract.client.lastname
                )
            console.print(table)
        else:
            click.secho(f"You are not allowed", fg="red")
    else:
        click.secho(f"You need to be logged", fg="red")
