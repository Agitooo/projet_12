from django.db import models
from apps.peoples.models import Customer, UserEmployee


class Contract(models.Model):

    PERMISSION_CONTRACT_NAME = 'contract'

    CONTRACT_NON_SIGNE = 1
    CONTRACT_SIGNE = 2

    CONTRACT_STATUS = [
        (CONTRACT_NON_SIGNE, 'non signé'),
        (CONTRACT_SIGNE, 'signé')
    ]

    client = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="client")
    contact = models.ForeignKey(UserEmployee, on_delete=models.DO_NOTHING, related_name="contact")
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=CONTRACT_STATUS)
    total_price = models.FloatField()
    remaining_price = models.FloatField()
    created_by = models.ForeignKey(UserEmployee, on_delete=models.DO_NOTHING, related_name="created_contrats")
    updated_by = models.ForeignKey(UserEmployee, on_delete=models.DO_NOTHING, related_name="updated_contrats")
    objects = models.Manager()

    class Meta:
        verbose_name = "contract"
        verbose_name_plural = "contracts"

    def __str__(self):
        return f"{self.client.firstname} {self.date_create}"
