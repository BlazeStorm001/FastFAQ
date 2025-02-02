# app/schemas/faq.py
from pydantic import BaseModel
from pydantic import ConfigDict

class FAQCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question: str
    answer: str
    language: str

class FAQ(FAQCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int

