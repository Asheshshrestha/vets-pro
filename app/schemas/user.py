from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(UserBase):
    name: str
    email: str
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
