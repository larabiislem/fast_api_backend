from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: Optional[bool] = True


class Responcemodal(Item):


    class Config:
        orm_mode = True