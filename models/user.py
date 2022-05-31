from pydantic import BaseModel


class UserBodyModel(BaseModel):
    age: int
    height: int
    weight: int
    email: str


class UserResModel(BaseModel):
    email: str
    name: str
    id: str
    height: int
    weight: int
    sex: int
    age: int
