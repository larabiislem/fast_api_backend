from . import scemat
from fastapi import FastAPI , Depends , HTTPException , status 
from sqlalchemy.orm import Session
from .database import engine , SessionLocal
from . import modal
from .routers import user, items

# This will create all tables defined with Base (including user)
modal.Base.metadata.create_all(bind=engine)



app = FastAPI()


app.include_router(user.router)
app.include_router(items.router)

# CRUD operations for Item
# post opération 

