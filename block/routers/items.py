from .. import scemat
from fastapi import FastAPI , Depends , HTTPException , status , APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import modal
from ..token import get_current_user


router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.post("/" , status_code=status.HTTP_201_CREATED)
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

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[scemat.Responcemodal] )
def get_items(db: Session = Depends(get_db), current_user: scemat.TokenData = Depends(get_current_user)):
    items = db.query(modal.Item).all()
    db.close()
    return items

@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(modal.Item).filter(modal.Item.id == item_id).first()
    db.close()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
  
    return item

@router.delete("/{item_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(modal.Item).filter(modal.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    db.delete(item)
    db.commit()
    db.close()
    
    return {"detail": "Item deleted successfully"}

# modify item price
@router.put("/{item_id}/{price}", status_code=status.HTTP_202_ACCEPTED)
def update_item(item_id: int, price: int, db: Session = Depends(get_db)):
    db_item = db.query(modal.Item).filter(modal.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
 
    db_item.price = price




    db.commit()