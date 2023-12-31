# Generated by Django 4.1.7 on 2023-08-03 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('peoples', '0001_initial'),
        ('contracts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='client', to='peoples.customer'),
        ),
        migrations.AddField(
            model_name='contract',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='contact', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_contrats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_contrats', to=settings.AUTH_USER_MODEL),
        ),
    ]
