from django.db import models
from apps.contracts.models import Contract
from apps.peoples.models import UserEmployee


class Event(models.Model):

    PERMISSION_EVENT_NAME = 'event'

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
    support = models.ForeignKey(UserEmployee, on_delete=models.DO_NOTHING,
                                blank=True, null=True, related_name="support_contact")
    objects = models.Manager()

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"

    def __str__(self):
        # return f"{self.location} : {self.date_start} au {self.date_end}"
        return f"{self.location}"
