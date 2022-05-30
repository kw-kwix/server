from pydantic import BaseModel


class RecommendBodyModel(BaseModel):
    email: str
