from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()



class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items")
def read_item():
    return {"item_id":' lmlm'}

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price, "item_is_offer": item.is_offer}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}







