from django.contrib import admin
from .models import UserEmployee, UserClient

admin.site.register(UserEmployee)
admin.site.register(UserClient)
