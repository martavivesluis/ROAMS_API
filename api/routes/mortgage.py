from fastapi import APIRouter
from api.models.mortgage import Mortgage
from api.models.client import Client
from api.schemas.mortgage import GetMortgage, PostMortgage
from typing import List

mortgage_router = APIRouter(prefix="/mortgage", tags=["Mortgage"])


@mortgage_router.get(
    "/",
    response_model=List[GetMortgage],
    responses={
        200: {
            "description": "List of retrieved Mortgages",
            "content": {
                "application/json": {
                    "examples": {
                        "success_example": {
                            "summary": "Mortgages",
                            "value": [
                                {
                                    "id": 13,
                                    "monthlyPayment": "322.67",
                                    "totalAmount": "11616.19",
                                    "client_id": "45129442S",
                                },
                                {
                                    "id": 14,
                                    "monthlyPayment": "322.67",
                                    "totalAmount": "11616.19",
                                    "client_id": "45129442S",
                                },
                            ],
                        }
                    }
                }
            },
        }
    },
)
async def all_mortgages():
    data = Mortgage.all()
    return await GetMortgage.from_queryset(data)


@mortgage_router.post("/", response_model=GetMortgage, responses={
        200: {
            "description": "Mortgage created successfully!",
            "content": {
                "application/json": {
                    "examples": {
                        "success_example": {
                            "summary": "Mortgage created",
                            "value": {
                                    "id": 13,
                                    "monthlyPayment": "322.67",
                                    "totalAmount": "11616.19",
                                    "client_id": "45129442S",
                                },
                        }
                    }
                }
            },
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "examples": {
                        "validation_error_example": {
                            "summary": "Validation error: DNI too long",
                            "value": {
                                "detail": [
                                    {
                                        "type": "string_too_long",
                                        "loc": ["body", "DNI"],
                                        "msg": "String should have at most 9 characters",
                                        "input": "45129442Ss",  # Ejemplo de DNI que causa el error
                                        "ctx": {"max_length": 9},
                                    }
                                ]
                            },
                        }
                    }
                }
            },
        },
    },
)
async def create_a_mortgage(body: PostMortgage
):

    DNI = body.DNI
    client = await Client.get_or_none(DNI=DNI)
    if client is None:
        return {"error": "Client not found"}

    requestedCapital = client.requestedCapital
    TAE = body.TAE
    repaymentTerm = body.repaymentTerm

    n = repaymentTerm * 12
    monthlyInterest = TAE / 1200

    monthlyPayment = requestedCapital * (
        (monthlyInterest) / (1 - ((1 + monthlyInterest) ** -n))
    )
    totalAmount = monthlyPayment * n

    # ahora creamos la entidad con el cliente asociado
    row = await Mortgage.create(
        client=client, monthlyPayment=monthlyPayment, totalAmount=totalAmount
    )
    return await GetMortgage.from_tortoise_orm(row)
