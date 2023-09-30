# Generated by Django 4.1.7 on 2023-09-04 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('peoples', '0003_customer_created_by_alter_useremployee_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]