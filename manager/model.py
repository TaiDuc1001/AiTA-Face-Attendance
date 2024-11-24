from pydantic import BaseModel, field_validator
from typing import List

class Student(BaseModel):
    name: str
    gender: bool
    embeddings: List[str]

    @field_validator('name')
    def name_must_be_alphabet(cls, value):
        if not value.isalpha():
            raise ValueError('Name must be alphabet')
        