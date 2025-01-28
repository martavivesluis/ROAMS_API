from pydantic import BaseModel, Field, field_validator
from tortoise.contrib.pydantic import pydantic_model_creator
from decimal import Decimal
from api.models.mortgage import Mortgage
from typing import Optional

#generamos un esquema de cliente en base al modelo de tortoise de cliente
class GetMortgage(pydantic_model_creator(Mortgage, name="Mortgage")):
    client_id: str


class PostMortgage(BaseModel):
    DNI: str = Field(..., min_length=9 ,max_length=9)
    TAE: Decimal
    repaymentTerm: Decimal

#https://www.interior.gob.es/opencms/es/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/
    @field_validator("DNI")
    def validate_dni(cls, value):
        if not value[:8].isdigit() or not value[-1].isalpha():
            raise ValueError("The first 8 characters of DNI must be numbers and the last character must be a letter")
        dni_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
        dni_number = int(value[:8])
        if value[-1] != dni_letters[dni_number % 23]:
            raise ValueError(f"The format for DNI is incorrect")
        return value

