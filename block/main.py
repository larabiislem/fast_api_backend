from . import scemat
from fastapi import FastAPI , Depends , HTTPException , status
from sqlalchemy.orm import Session
from .database import engine , SessionLocal
from . import modal
from .hacing import Hash

# This will create all tables defined with Base (including user)
modal.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations for Item
# post opération 
@app.post("/blokkk" , status_code=status.HTTP_201_CREATED)
def read_root(item: scemat.Item , db: Session = Depends(get_db)):
    new_item = modal.Item(
        name=item.name,
        description=item.description,
        price=item.price,
        is_available=item.is_available,
        owner_id=item.owner_id
        
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    db.close()

    return new_item

@app.get("/blokkk", status_code=status.HTTP_200_OK, response_model=list[scemat.Responcemodal])
def get_items(db: Session = Depends(get_db)):
    items = db.query(modal.Item).all()
    db.close()
    return items

@app.get("/blokkk/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(modal.Item).filter(modal.Item.id == item_id).first()
    db.close()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
  
    return item

@app.delete("/blokkk/{item_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(modal.Item).filter(modal.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    db.delete(item)
    db.commit()
    db.close()
    
    return {"detail": "Item deleted successfully"}

# modify item price
@app.put("/blokkk/{item_id}/{price}", status_code=status.HTTP_202_ACCEPTED)
def update_item(item_id: int, price: int, db: Session = Depends(get_db)):
    db_item = db.query(modal.Item).filter(modal.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
 
    db_item.price = price




    db.commit()
    
    
    return {"detail": "Item updated successfully", "item_id": item_id, "new_price": price}


@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=scemat.UserResponse)
def creat_user(user: scemat.User, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(modal.user).filter(modal.user.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


    hashed_password = Hash.hash_password(user.hashed_password)


    new_user = modal.user(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users", status_code=status.HTTP_200_OK, response_model=list[scemat.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(modal.user).all()
    return users

