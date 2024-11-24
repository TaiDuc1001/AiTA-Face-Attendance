from pydantic import BaseModel, field_validator
from typing import List
import re
import random

def generate_student_code():
    suffix = ''.join(random.choices('0123456789', k=4))
    prefix = random.choice('QHCS')
    term = random.choice([str(i) for i in range(16, 20)])
    return f"{prefix}E{term}{suffix}"

class Student(BaseModel):
    name: str
    code: str
    gender: bool
    embeddings: List[str]

    @field_validator('name')
    def name_must_be_alphabet(cls, value):
        if not all(part.isalpha() for part in value.split()):
            raise ValueError('Name must contain only alphabetic characters and spaces')
        return value
    
    @field_validator('code')
    def code_must_be_valid(cls, value):
        pattern = r"^[QHCS]E(16|17|18|19)\d{4}$"
        if not re.match(pattern, value):
            raise ValueError('Invalid student code format')
        return value