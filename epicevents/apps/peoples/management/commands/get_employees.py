import djclick as click
from django.core.management import BaseCommand
from rich.console import Console
from rich.table import Table

from apps.peoples.models import UserEmployee
from django_token.models import Token
from settings.settings import VIEW

console = Console()


@click.command()
@click.option('--groupe', '-grid', prompt=True, default='ALL',
              type=click.Choice(['COMMERCIAL', 'GESTION', 'SUPPORT', 'ALL'], case_sensitive=False))
def get_employees(groupe):
    """
        Show employee by group
    """

    user = UserEmployee()
    token = user.token_is_valid()

    # TODO : mettre en décorateur le user.token_is_valid() et isinstance
    if isinstance(token, Token):

        is_allowed = user.has_permission(token.user, VIEW + UserEmployee.PERMISSION_USER_NAME)

        if is_allowed:

            match groupe:
                case 'COMMERCIAL':
                    employees = UserEmployee.objects.filter(
                        is_active=True,
                        department=UserEmployee.EMPLOYEE_COMMERCIAL
                    )
                case 'GESTION':
                    employees = UserEmployee.objects.filter(
                        is_active=True,
                        department=UserEmployee.EMPLOYEE_GESTION
                    )
                case 'SUPPORT':
                    employees = UserEmployee.objects.filter(
                        is_active=True,
                        department=UserEmployee.EMPLOYEE_SUPPORT
                    )
                case 'ALL':
                    employees = UserEmployee.objects.filter(
                        is_active=True,
                    )
                case _:
                    employees = UserEmployee.objects.filter(
                        is_active=True,
                    )

            table = Table(show_header=True)
            table.add_column("ID Contact")
            table.add_column("Firstname")
            table.add_column("Lastname")
            table.add_column("Email")
            table.add_column("Phone")

            if employees.count() == 0:
                click.secho("No contact employee available", fg="red")
            else:
                for employee in employees:
                    table.add_row(str(employee.pk), employee.first_name,
                                  employee.last_name, employee.email, employee.phone)
                console.print(table)
        else:
            click.secho(f"You are not allowed", fg="red")
    else:
        click.secho(f"You need to be logged", fg="red")
