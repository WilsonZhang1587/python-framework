from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, schemas
from ..repository import user

router = APIRouter(
  prefix="/user",
  tags=['Users']
)

# ----- user get -------------------------------------------------------------------------------------------------------------------------

@router.get('/{id}/', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
  return user.show(id, db)

# ----- user post -------------------------------------------------------------------------------------------------------------------------

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
  return user.create(request, db)