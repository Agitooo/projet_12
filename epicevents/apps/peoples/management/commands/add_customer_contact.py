import djclick as click
from django.core.management import BaseCommand
from rich.console import Console
from rich.table import Table

from apps.peoples.models import Customer, UserEmployee
from django_token.models import Token
from settings.settings import CHANGE

console = Console()


@click.command()
@click.option('--customer_id', '-cuid', prompt=True)
@click.option('--contact_id', '-coid', prompt=True)
def command(customer_id, contact_id):
    """
        Add contact to customer
    """

    user = UserEmployee()
    token = user.token_is_valid()

    if isinstance(token, Token):

        is_allowed = user.has_permission(token.user, CHANGE + Customer.PERMISSION_CUSTOMER_NAME)

        if is_allowed:

            if not isinstance(customer_id, int):
                click.secho(f"Invalid customer", fg="red")
                exit()

            if not isinstance(contact_id, int):
                click.secho(f"Invalid contact", fg="red")
                exit()

            try:
                contact = UserEmployee.objects.get(pk=contact_id)

                if contact.department == UserEmployee.EMPLOYEE_SUPPORT:
                    customer = Customer.objects.get(actif=True, pk=customer_id)
                    # Uniquement le commercial qui a créé le contact peut le modifier
                    if customer.created_by == token.user:
                        customer.contact = contact
                        customer.save()
                        table = Table(show_header=True)
                        table.add_column("Customer ID")
                        table.add_column("Customer Firstname")
                        table.add_column("Customer Lastname")
                        table.add_column("Email")
                        table.add_column("Phone")
                        table.add_column("Company")
                        table.add_column("Contact ID")
                        table.add_column("Contact Firstname")
                        table.add_column("Contact Lastname")
                        table.add_row(
                            str(customer.pk),
                            customer.firstname, customer.lastname, customer.email, customer.phone, customer.company,
                            str(customer.contact.pk),
                            customer.contact.first_name, customer.contact.last_name
                        )
                        console.print(table)
                        click.secho("Contact add to customer successfully", fg="green")
                    else:
                        click.secho("Authorization refused", fg="red")
                else:
                    click.secho("Contact is not in support team", fg="red")
            except UserEmployee.DoesNotExist:
                click.secho("Invalid contact", fg="red")
            except Customer.DoesNotExist:
                click.secho("Invalid customer", fg="red")
        else:
            click.secho(f"You are not allowed", fg="red")
    else:
        click.secho(f"You need to be logged", fg="red")
