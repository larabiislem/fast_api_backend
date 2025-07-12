from . import scemat
from fastapi import FastAPI


app = FastAPI()
@app.post("/blokkk")
def read_root(item: scemat.Item):
    return {"Hello": item}