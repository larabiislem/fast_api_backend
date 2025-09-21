from block import scemat
from block.database import engine, SessionLocal
from block import modal
from block.routers import user, items
from fastapi import FastAPI

modal.Base.metadata.create_all(bind=engine)



app = FastAPI()





app.include_router(user.router)
app.include_router(items.router)



