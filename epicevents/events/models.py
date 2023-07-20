from django.db import models
from contracts.models import Contract
from users.models import UserEmployee


class Event(models.Model):

    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING, related_name="contract")
    location = models.CharField(max_length=1024)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    total_people = models.IntegerField()
    comment = models.CharField(max_length=2048)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)
    created_by = models.ForeignKey(UserEmployee, on_delete=models.DO_NOTHING, related_name="created_events")
    updated_by = models.ForeignKey(UserEmployee, on_delete=models.DO_NOTHING, related_name="updated_events")
    objects = models.Manager()

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"

    def __str__(self):
        return f"{self.location} : {self.date_start} au {self.date_end}"