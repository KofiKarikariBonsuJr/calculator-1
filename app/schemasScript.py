from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class CalcType(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalcType

    @validator("b")
    def check_divide_by_zero(cls, v, values):
        if "type" in values and values["type"] == CalcType.divide and v == 0:
            raise ValueError("Division by zero not allowed")
        return v

class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalcType
    result: Optional[float]
    user_id: Optional[int]
    created_at: datetime
    class Config:
        orm_mode = True
