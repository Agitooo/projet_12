import djclick as click
from django.core.management import BaseCommand
from rich.console import Console
from rich.table import Table

from apps.peoples.models import Customer, UserEmployee
from django_token.models import Token
from settings.settings import ADD

console = Console()


@click.command()
@click.option('--username', '-un', prompt=True)
@click.option('--password', '-pw', prompt=True, hide_input=True)
@click.option('--firstname', '-fn', prompt=True)
@click.option('--lastname', '-ln', prompt=True)
@click.option('--email', '-e', prompt=True)
@click.option('--phone', '-p', prompt=True)
@click.option('--department', '-dpt', prompt=True,
              type=click.Choice(['COMMERCIAL', 'GESTION', 'SUPPORT'], case_sensitive=False))
def add_employee(username, password, firstname, lastname, email, phone, department):
    """
        Create employee
    """

    user = UserEmployee()
    token = user.token_is_valid()

    if isinstance(token, Token):

        is_allowed = user.has_permission(token.user, ADD + UserEmployee.PERMISSION_EMPLOYEE_NAME)

        if is_allowed:

            new_employee = UserEmployee()

            match department:
                case 'COMMERCIAL':
                    dpt_id = new_employee.EMPLOYEE_COMMERCIAL
                case 'GESTION':
                    dpt_id = new_employee.EMPLOYEE_GESTION
                case 'SUPPORT':
                    dpt_id = new_employee.EMPLOYEE_SUPPORT
                case _:
                    dpt_id = None
                    click.secho("Department invalid", fg="red")
                    exit()

            employee = new_employee.create_user(username, password, email, lastname, firstname, phone, dpt_id)

            if employee:
                table = Table(show_header=True)
                table.add_column("ID Contact")
                table.add_column("Firstname")
                table.add_column("Lastname")
                table.add_column("Email")
                table.add_column("Phone")
                table.add_row(str(employee.pk), employee.first_name,
                              employee.last_name, employee.email, employee.phone)
                console.print(table)
                click.secho("Employee created", fg="green")
            else:
                click.secho("Employee not created", fg="red")
        else:
            click.secho(f"You are not allowed", fg="red")
    else:
        click.secho(f"You need to be logged", fg="red")
