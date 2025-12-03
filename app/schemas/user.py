from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str   # plain text

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: str

    class Config:
        orm_mode = True
