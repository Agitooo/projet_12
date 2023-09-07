import djclick as click
from django.core.management import BaseCommand
from rich.console import Console
from rich.table import Table

from apps.peoples.models import UserEmployee
from apps.contracts.models import Contract
from apps.events.models import Event
from django_token.models import Token
from settings.settings import CHANGE

console = Console()


@click.command()
@click.option('--event_id', '-cid', prompt=True)
@click.option('--support_id', '-sid', prompt=True)
def update_event(event_id, support_id):
    """
        update event
    """

    user = UserEmployee()
    token = user.token_is_valid()

    if isinstance(token, Token):

        is_allowed = user.has_permission(token.user, CHANGE + Event.PERMISSION_EVENT_NAME)

        if is_allowed:

            try:

                event = Event.objects.get(pk=event_id)
                support = UserEmployee.objects.get(pk=support_id)

                # Le support saisi, n'est pas dans le département support des employés
                if support.department != UserEmployee.EMPLOYEE_SUPPORT:
                    click.secho("support_id is not support employee", fg="red")

                event.support = support
                event.save()

                if event:
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
                    click.secho("Event updated", fg="green")
                else:
                    click.secho("Event not found", fg="red")
            except Event.DoesNotExist:
                click.secho("Invalid event", fg="red")
            except UserEmployee.DoesNotExist:
                click.secho("Invalid Support", fg="red")
        else:
            click.secho(f"You are not allowed", fg="red")
    else:
        click.secho(f"You need to be logged", fg="red")
