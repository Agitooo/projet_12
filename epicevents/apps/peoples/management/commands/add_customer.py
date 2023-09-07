import djclick as click
from django.core.management import BaseCommand
from rich.console import Console
from rich.table import Table

from apps.peoples.models import Customer, UserEmployee
from django_token.models import Token
from settings.settings import ADD

console = Console()


@click.command()
@click.option('--firstname', '-fn', prompt=True)
@click.option('--lastname', '-ln', prompt=True)
@click.option('--email', '-e', prompt=True)
@click.option('--phone', '-p', prompt=True)
@click.option('--company', '-c', prompt=True)
def command(firstname, lastname, email, phone, company):
    """
        Create customer
    """

    user = UserEmployee()
    token = user.token_is_valid()

    if isinstance(token, Token):

        is_allowed = user.has_permission(token.user, ADD + Customer.PERMISSION_CUSTOMER_NAME)

        if is_allowed:

            customer = Customer()
            customer.firstname = firstname
            customer.lastname = lastname
            customer.email = email
            customer.phone = phone
            customer.company = company
            customer.created_by = token.user
            customer.save()
            customer_pk = customer.pk

            if customer_pk:
                table = Table(show_header=True)
                table.add_column("ID customer")
                table.add_column("Firstname")
                table.add_column("Lastname")
                table.add_column("Email")
                table.add_column("Phone")
                table.add_column("Company")
                table.add_row(str(customer_pk), firstname, lastname, email, phone, company)
                console.print(table)
                click.secho("Customer created", fg="green")
            else:
                click.secho("Customer not created", fg="red")
        else:
            click.secho(f"You are not allowed", fg="red")
    else:
        click.secho(f"You need to be logged", fg="red")
