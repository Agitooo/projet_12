import djclick as click
from django.core.management import BaseCommand
from rich.console import Console
from rich.table import Table
from datetime import datetime

from apps.peoples.models import Customer, UserEmployee
from apps.contracts.models import Contract
from apps.events.models import Event
from django_token.models import Token
from settings.settings import ADD

console = Console()


@click.command()
@click.option('--contract_id', '-cid', prompt=True)
@click.option('--location', '-l', prompt=True)
@click.option('--date_start', '-ds', prompt=True)
@click.option('--date_end', '-de', prompt=True)
@click.option('--total_people', '-p', prompt=True)
@click.option('--comment', '-c', prompt=True, default='')
def add_event(contract_id, location, date_start, date_end, total_people, comment=""):
    """
        Create event
    """
    user = UserEmployee()
    token = user.token_is_valid()

    if isinstance(token, Token):

        is_allowed = user.has_permission(token.user, ADD + Event.PERMISSION_EVENT_NAME)

        if is_allowed:

            try:
                contract = Contract.objects.get(pk=contract_id)

                date_start = date_start + ":00"
                date_end = date_end + ":00"
                date_start_object = datetime.strptime(date_start, '%d/%m/%Y %H:%M:%S')
                date_end_object = datetime.strptime(date_end, '%d/%m/%Y %H:%M:%S')

                event = Event()
                event.contract = contract
                event.location = location
                event.date_start = date_start_object
                event.date_end = date_end_object
                event.total_people = total_people
                event.comment = comment
                event.created_by = token.user
                event.updated_by = token.user
                event.save()
                event_pk = event.pk

                if event_pk:
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
                    table.add_row(
                        str(event.pk),
                        event.location, event.date_start, event.date_end, str(event.total_people), event.comment,
                        str(event.contract.pk),
                        str(event.contract.client.pk), event.contract.client.firstname, event.contract.client.lastname
                    )
                    console.print(table)
                    click.secho("Event created", fg="green")
                else:
                    click.secho("Event not created", fg="red")
            except Contract.DoesNotExist:
                click.secho("Contract does not exist", fg="red")
        else:
            click.secho(f"You are not allowed", fg="red")
    else:
        click.secho(f"You need to be logged", fg="red")

