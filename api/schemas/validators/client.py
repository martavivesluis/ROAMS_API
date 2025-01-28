
from pydantic import FieldValidationInfo
from fastapi import APIRouter, Depends, HTTPException

#https://www.interior.gob.es/opencms/es/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/
def validate_dni(value: str, _: FieldValidationInfo = None) -> str:
    if not value[:8].isdigit() or not value[-1].isalpha():
        raise HTTPException(status_code=422, detail="The first 8 characters of DNI must be numbers and the last character must be a letter")
    dni_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    dni_number = int(value[:8])
    if value[-1] != dni_letters[dni_number % 23]:
        raise HTTPException(status_code=422, detail="The DNI's format is incorrect")
    return value