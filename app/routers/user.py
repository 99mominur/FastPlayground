from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status, Depends, APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(payload: schemas.PayloadUser, db: Session = Depends(get_db)):
    try:
        hashed_password = utils.hash_password(payload.password)
        payload.password = hashed_password
        user = models.User(**payload.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/{id}", response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(get_db)):
    """Retrieve a single user by ID"""
    try:
        user = db.query(models.User).filter(models.User.id == id).first()
        if user is None:
            return Response(
                content="User not found", status_code=status.HTTP_404_NOT_FOUND
            )

        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
