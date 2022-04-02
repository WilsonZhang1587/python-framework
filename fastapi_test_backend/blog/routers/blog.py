from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.orm import Session
from .. import database, models, schemas, oauth2

router = APIRouter(
  prefix="/blog",
  tags=['Blogs']
)

# ----- blog get all -------------------------------------------------------------------------------------------------------------------------

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
  blogs = db.query(models.Blog).all()

  return blogs

# ----- blog get one -------------------------------------------------------------------------------------------------------------------------

@router.get('/{id}/', status_code=200, response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(database.get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()

  if not blog:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'blog with the id:{id} is not available')
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return { 'detail': f'blog with the id:{id} is not available' }

  return blog

# ----- blog post -------------------------------------------------------------------------------------------------------------------------

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
  new_blog = models.Blog(
    title=request.title,
    body=request.body,
    user_id=request.user_id
  )
  
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)

  return new_blog

# ----- blog put -------------------------------------------------------------------------------------------------------------------------

@router.put('/{id}/', status_code=status.HTTP_202_ACCEPTED)
def destory(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  
  if not blog.first():
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'blog with the id:{id} is not found')
  
  blog.update(dict(request))
  db.commit()

  return { 'detail': 'Done' }

# ----- blog delete -------------------------------------------------------------------------------------------------------------------------

@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
def destory(id, db: Session = Depends(database.get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)

  if not blog.first():
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'blog with the id:{id} is not found')

  blog.delete(synchronize_session=False)
  db.commit()

  return { 'detail': 'Done' }