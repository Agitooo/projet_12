import djclick as click
from django.core.management import BaseCommand
from rich.console import Console
from rich.table import Table

from apps.peoples.models import Customer, UserEmployee
from apps.contracts.models import Contract
from django_token.models import Token
from settings.settings import CHANGE

console = Console()


@click.command()
@click.option('--contract_id', '-cid', prompt=True)
@click.option('--status', '-st', prompt=True, default='')
@click.option('--remaining_price', '-rm', prompt=True, default='')
def add_contract(contract_id, status="", remaining_price=""):
    """
        Update contract
    """

    user = UserEmployee()
    token = user.token_is_valid()

    if isinstance(token, Token):

        is_allowed = user.has_permission(token.user, CHANGE + Contract.PERMISSION_CONTRACT_NAME)
        if is_allowed:

            if status == "" and remaining_price == "":
                click.secho("no data to update", fg="red")
                exit()

            contract = Contract.objects.filter(pk=contract_id).first()

            # Seul le commercial du client peut modifier le contrat du client ou un gestionnaire
            if (
                    contract.client.created_by == token.user
                    and
                    token.user.department == UserEmployee.EMPLOYEE_COMMERCIAL
            ) \
                    or \
                    (token.user.department == UserEmployee.EMPLOYEE_GESTION):
                if status != "":
                    contract.status = Contract.CONTRACT_SIGNE
                if remaining_price != "":
                    contract.remaining_price = remaining_price
                contract.updated_by = token.user
                contract.save()

                if contract:
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
                    click.secho("Contract updated", fg="green")
                else:
                    click.secho("Contract not found", fg="red")
            else:
                click.secho("Authorization refused", fg="red")
        else:
            click.secho(f"You are not allowed", fg="red")
    else:
        click.secho(f"You need to be logged", fg="red")
