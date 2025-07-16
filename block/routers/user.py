from .. import scemat
from fastapi import FastAPI , Depends , HTTPException , status , APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import modal
from ..hacing import Hash
from datetime import timedelta
from ..token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES



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


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: scemat.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(modal.user).filter(modal.user.email == user.email).first()
    if not db_user or not Hash.verify_password(user.hashed_password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return scemat.Token(access_token=access_token, token_type="bearer")

    
    return {"message": "Login successful"}

