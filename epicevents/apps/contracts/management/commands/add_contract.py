import djclick as click
from django.core.management import BaseCommand
from rich.console import Console
from rich.table import Table

from apps.peoples.models import Customer, UserEmployee
from apps.contracts.models import Contract
from django_token.models import Token
from settings.settings import ADD

console = Console()


@click.command()
@click.option('--customer_id', '-cuid', prompt=True)
@click.option('--contact_id', '-ln', prompt=True)
@click.option('--total_price', '-p', prompt=True)
def add_contract(customer_id, contact_id, total_price):
    """
        Create contract
    """

    user = UserEmployee()
    token = user.token_is_valid()

    if isinstance(token, Token):

        is_allowed = user.has_permission(token.user, ADD + Contract.PERMISSION_CONTRACT_NAME)

        if is_allowed:

            try:
                customer = Customer.objects.get(pk=customer_id)
                contact = UserEmployee.objects.get(pk=contact_id)

                if not isinstance(total_price, int) or not isinstance(total_price, float):
                    click.secho(f"Invalid price", fg="red")
                    exit()

                contract = Contract()
                contract.client = customer
                contract.contact = contact
                contract.status = Contract.CONTRACT_NON_SIGNE
                contract.total_price = total_price
                contract.remaining_price = total_price
                contract.created_by = token.user
                contract.updated_by = token.user
                contract.save()
                contract_pk = contract.pk

                if contract_pk:
                    table = Table(show_header=True)
                    table.add_column("Customer ID")
                    table.add_column("Firstname")
                    table.add_column("Lastname")
                    table.add_column("Commercial ID")
                    table.add_column("Firstname")
                    table.add_column("Lastname")
                    table.add_column("Contract ID")
                    table.add_column("Status")
                    table.add_column("Total price €")
                    table.add_column("Remaining price €")
                    table.add_row(
                        str(contract.client.pk),
                        contract.client.firstname, contract.client.lastname,
                        str(contract.contact.pk),
                        contract.contact.first_name, contract.contact.last_name,
                        str(contract.pk),
                        Contract.CONTRACT_STATUS[contract.status - 1][1],
                        f"{contract.total_price} €", f"{contract.remaining_price} €"
                    )
                    console.print(table)
                    click.secho("Contract created", fg="green")
                else:
                    click.secho("Customer not created", fg="red")
            except Customer.DoesNotExist:
                click.secho("Invalid customer", fg="red")
            except UserEmployee.DoesNotExist:
                click.secho("Invalid contact", fg="red")
        else:
            click.secho(f"You are not allowed", fg="red")
    else:
        click.secho(f"You need to be logged", fg="red")
