
from tortoise.models import Model
from tortoise import fields

class Client(Model):
    DNI = fields.CharField(max_length=9, min_length=9,primary_key=True)
    name = fields.CharField(max_length=60)
    email = fields.CharField(unique=True, max_length=60)
    requestedCapital = fields.DecimalField(max_digits=10, decimal_places=2)

    
