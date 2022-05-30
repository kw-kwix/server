from pydantic import BaseModel


class LoginBodyModel(BaseModel):
    email: str
    password: str


class SignUpBodyModel(BaseModel):
    id: str
    email: str
    password: str
    name: str
    sex: int
    birthdayDate: int
    phoneNumber: str
