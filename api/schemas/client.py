from pydantic import BaseModel, Field, field_validator, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator
from decimal import Decimal
from api.models.client import Client
from typing import Optional
from .validators.client import validate_dni

#generamos un esquema de cliente en base al modelo de tortoise de cliente
GetClient = pydantic_model_creator(Client, name="Client")


class DNISchema(BaseModel):
    DNI: str = Field(None, min_length=9 ,max_length=9)
    
    @field_validator("DNI")
    def validate_dni(cls, value):
        return validate_dni(value)

class PutClient(BaseModel):
    DNI: str = Field(..., min_length=9 ,max_length=9)
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    requestedCapital: Optional[Decimal] = None

    @field_validator("DNI")
    def validate_dni(cls, value):
        return validate_dni(value)

class PostClient(BaseModel):
    name: str
    DNI: str = Field(..., min_length=9, max_length=9)
    email: EmailStr
    requestedCapital: Decimal

    @field_validator("DNI")
    def validate_dni(cls, value):
        return validate_dni(value)

class DeleteClientResponse(BaseModel):
    message: str

