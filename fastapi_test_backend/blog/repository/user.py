from fastapi import HTTPException, status
from ..hashing import Hash
from .. import models

def show(id: str, db):
  user = db.query(models.User).filter(models.User.id == id).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id:{id} is not available")

  return user

def create(request, db):
  new_user = models.User(
    name = request.name,
    email = request.email,
    password = Hash.bcrypt(request.password)
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user