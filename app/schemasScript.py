from pydantic import BaseModel
from enum import Enum

class CalcType(str, Enum):
    add = "add"
    sub = "sub"

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalcType

    def perform(self):
        if self.type == CalcType.add:
            return self.a + self.b
        if self.type == CalcType.sub:
            return self.a - self.b

class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalcType
    result: float

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    username: str
    password: str
