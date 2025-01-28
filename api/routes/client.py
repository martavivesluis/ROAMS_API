from fastapi import APIRouter, Depends, HTTPException
from api.models.client import Client
from api.schemas.client import (
    GetClient,
    PostClient,
    DNISchema,
    PutClient,
    DeleteClientResponse,
)
from typing import List

client_router = APIRouter(prefix="/client", tags=["client"])


@client_router.get(
    "/",
    response_model=List[GetClient],
    responses={
        200: {
            "description": "List of clients retrieved",
            "content": {
                "application/json": {
                    "examples": {
                        "example_1": {
                            "summary": "List of clients",
                            "value": [
                                {
                                    "DNI": "45129442S",
                                    "email": "martavivesluis@gmail.com",
                                    "name": "Marta Vives",
                                    "requestedCapital": 32000,
                                },
                                {
                                    "DNI": "65004204V",
                                    "email": "jesus@gmail.com",
                                    "name": "Jesus Hidalgo",
                                    "requestedCapital": 85000,
                                },
                            ],
                        }
                    },
                }
            },
        }
    },
)
async def all_clients():
    data = Client.all()
    return await GetClient.from_queryset(data)


@client_router.post(
    "/",
    response_model=GetClient,
    responses={
        200: {
            "description": "Client created successfully!",
            "content": {
                "application/json": {
                    "examples": {
                        "success_example": {
                            "summary": "Client created",
                            "value": {
                                "name": "Marta Vives",
                                "DNI": "45129442S",
                                "email": "martavivesluis@gmail.com",
                                "requestedCapital": 32000,
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
async def create_client(body: PostClient):
    row = await Client.create(**body.model_dump(exclude_unset=True))
    return await GetClient.from_tortoise_orm(row)


@client_router.get(
    "/{DNI}",
    response_model=GetClient,
    responses={
        200: {
            "description": "Client created successfully!",
            "content": {
                "application/json": {
                    "examples": {
                        "success_example": {
                            "summary": "Client created",
                            "value": {
                                "name": "Marta Vives",
                                "DNI": "45129442S",
                                "email": "martavivesluis@gmail.com",
                                "requestedCapital": 32000,
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
                                        "input": "45129442Ss",
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
async def client_by_DNI(Schema: str = Depends(DNISchema)):
    client = await Client.get_or_none(DNI=Schema.DNI)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return await GetClient.from_tortoise_orm(client)


@client_router.put("/",response_model=GetClient,
    responses={
        200: {
            "description": "Client modified successfully!",
            "content": {
                "application/json": {
                    "examples": {
                        "success_example": {
                            "summary": "Client modified",
                            "value": {
                                "name": "Marta Vives",
                                "DNI": "45129442S",
                                "email": "martavivesluis@gmail.com",
                                "requestedCapital": 32000,
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
    })
async def put_client(body: PutClient, response_model=GetClient):
    client = await Client.get_or_none(DNI=body.DNI)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    await client.update_from_dict(body.model_dump(exclude_unset=True, exclude={"DNI"}))
    await client.save()
    return await GetClient.from_tortoise_orm(client)


@client_router.delete(
    "/{DNI}",
    response_model=DeleteClientResponse,
    responses={
        404: {
            "description": "Client not found",
            "content": {
                "application/json": {"example": {"detail": "Client not found"}}
            },
        },
        200: {
            "description": "Client deleted sucessfully",
            "content": {
                "application/json": {
                    "example": {"message": "Client deleted sucessfully"}
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
                                        "input": "45129442Ss",
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
async def delete_client(Schema: str = Depends(DNISchema)):
    client = await Client.get_or_none(DNI=Schema.DNI)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    await client.delete()
    return {"message": "Client deleted sucessfully"}
