from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: Optional[bool] = True
    owner_id: Optional[int] = None

class User(BaseModel):
    name: str
    email: str
    hashed_password: str
    is_active: Optional[bool] = True



class Responcemodal(Item):


    class Config:
        orm_mode = True


class UserResponse(User):
    name: str
    email: str
    items: Optional[list[Item]] = None

    class Config:
        orm_mode = True