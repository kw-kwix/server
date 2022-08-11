from pydantic import BaseModel


class UserBodyModel(BaseModel):
    age: int
    sex: int
    height: int
    weight: int
    email: str
    bmi: int
    during: int
    


class UserResModel(BaseModel):
    email: str
    name: str
    id: str
    height: int
    weight: int
    sex: int
    age: int
    during: int
    bmi: int
    

