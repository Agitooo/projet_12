from django.db import models
from users.models import UserClient, UserEmployee


class Contract(models.Model):

    CONTRACT_NON_SIGNE = 1
    CONTRACT_SIGNE = 2

    CONTRACT_STATUS = [
        (CONTRACT_NON_SIGNE, 'non signé'),
        (CONTRACT_SIGNE, 'signé')
    ]

    client = models.ForeignKey(UserClient, on_delete=models.DO_NOTHING, related_name="client")
    contact = models.ForeignKey(UserEmployee, on_delete=models.DO_NOTHING, related_name="contact")
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=CONTRACT_STATUS)
    total_price = models.FloatField()
    remaining_price = models.FloatField()
    created_by = models.ForeignKey(UserEmployee, on_delete=models.DO_NOTHING, related_name="created_contrats")
    updated_by = models.ForeignKey(UserEmployee, on_delete=models.DO_NOTHING, related_name="updated_contrats")

    class Meta:
        verbose_name = "contract"
        verbose_name_plural = "contracts"

    def __str__(self):
        return f"{self.client.name} {self.date_create}"
