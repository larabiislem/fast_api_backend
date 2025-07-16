from .. import scemat
from fastapi import FastAPI , Depends , HTTPException , status , APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import modal
from ..hacing import Hash


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=scemat.UserResponse)
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

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[scemat.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(modal.user).all()
    return users

