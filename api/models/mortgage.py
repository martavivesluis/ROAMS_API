from tortoise.models import Model
from tortoise import fields

from .client import Client

class Mortgage(Model):
    id = fields.IntField(pk=True)
    monthlyPayment = fields.DecimalField(max_digits=10, decimal_places=2)
    totalAmount = fields.DecimalField(max_digits=10, decimal_places=2)
    #one client associated with many entities
    client: fields.ForeignKeyRelation[Client] = fields.ForeignKeyField(
        "models.Client", related_name="entities"
    )

    class Meta:
        table = "mortgages"