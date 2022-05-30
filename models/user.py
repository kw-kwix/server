from pydantic import BaseModel


class UserBodyModel(BaseModel):
    age: int
    height: int
    weight: int
    email: str
