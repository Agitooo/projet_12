import djclick as click
from django.core.management import BaseCommand
from rich.console import Console
from rich.table import Table

from apps.peoples.models import Customer, UserEmployee
# import apps.peoples.decorators as decorators
from django_token.models import Token
from settings.settings import VIEW

console = Console()


@click.command()
# @decorators.is_log()
def get_customers():
    """
        Show all customer
    """

    user = UserEmployee()
    token = user.token_is_valid()

    # On a bien un token d'authentification valide pour ce user
    if isinstance(token, Token):

        # On regarde si le user à la permission de voir les clients
        is_allowed = user.has_permission(token.user, VIEW + Customer.PERMISSION_CUSTOMER_NAME)

        if is_allowed:
            table = Table(show_header=True)
            table.add_column("ID Customer")
            table.add_column("Firstname")
            table.add_column("Lastname")
            table.add_column("Email")
            table.add_column("Phone")
            table.add_column("Company")
            customers = Customer.objects.filter(actif=True)
            for customer in customers:
                table.add_row(str(customer.pk), customer.firstname, customer.lastname,
                              customer.email, customer.phone, customer.company)
            console.print(table)
        else:
            click.secho(f"You are not allowed", fg="red")
    else:
        click.secho(f"You need to be logged", fg="red")
