import djclick as click
from django.core.management import BaseCommand
from rich.console import Console
from rich.table import Table

from apps.peoples.models import UserEmployee, Customer
from apps.contracts.models import Contract
from django_token.models import Token
from settings.settings import VIEW

console = Console()


@click.command()
@click.option('--filters', '-fil', prompt=True, default='ALL',
              type=click.Choice(
                  ['MY', 'ALL', 'SIGNE', 'NON SIGNE', 'TOTALLY PAY', 'NOT TOTALLY PAY'],
                  case_sensitive=False
              ))
def get_contracts(filters):
    """
        Show all contracts
    """

    user = UserEmployee()
    token = user.token_is_valid()

    if isinstance(token, Token):
        is_allowed = user.has_permission(token.user, VIEW + Contract.PERMISSION_CONTRACT_NAME)

        if is_allowed:

            # Depuis python 3.10 match / case
            match filters:
                case 'MY':
                    contracts = Contract.objects.filter(client__created_by=token.user)
                case 'ALL':
                    contracts = Contract.objects.all()
                case 'SIGNE':
                    contracts = Contract.objects.filter(status=Contract.CONTRACT_SIGNE)
                case 'NON SIGNE':
                    contracts = Contract.objects.filter(status=Contract.CONTRACT_NON_SIGNE)
                case 'TOTALLY PAY':
                    contracts = Contract.objects.filter(remaining_price=0.0)
                case 'NOT TOTALLY PAY':
                    contracts = Contract.objects.filter().exclude(remaining_price=0.0)
                case _:
                    contracts = Contract.objects.all()

            if contracts:
                table = Table(show_header=True)
                table.add_column("Customer ID")
                table.add_column("Firstname")
                table.add_column("Lastname")
                table.add_column("Commercial ID")
                table.add_column("Firstname")
                table.add_column("Lastname")
                table.add_column("Contract ID")
                table.add_column("Status")
                table.add_column("Total price")
                table.add_column("Remaining price")

                for contract in contracts:
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
            else:
                click.secho(f"No contract found", fg="red")
        else:
            click.secho(f"You are not allowed", fg="red")
    else:
        click.secho(f"You need to be logged", fg="red")
