from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from . import models, schemas
from .database import engine, get_db, SessionLocal
from .routers import authentication, blog, user

app = FastAPI()

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)

@app.post('/test_post', status_code=status.HTTP_201_CREATED)
def createTest(request: schemas.Test, db: Session = Depends(get_db)):
  for i in range(30):
    new_test = models.Test(
      name = request.name + f"{i + 1}",
      title = request.title + f"{i + 1}",
      date = request.date,
      number = request.number + round((i + 1)/2),
    )
    db.add(new_test)
    db.commit()
    db.refresh(new_test)

  return new_test

@app.post('/test_get', status_code=200)
def getTest(request: schemas.Test2, db: Session = Depends(get_db)):
  params = {
    'name': request.name,
    'title': request.title
  }

  test = db.query(models.Test).filter_by(**params).filter(models.Test.number.between(0, 5)).all()

  test = db.query(models.Test).filter(
    models.Test.name == request.name,
    models.Test.title == request.title,
    models.Test.number >= 0,
    models.Test.number < 6
  ).all()

  return test

# 自動化處理資料
def test_function():
  db = SessionLocal()

  for i in range(30):
    new_blog = models.Blog(
      title=f"title{i+1}",
      body=f"body{i+1}",
      user_id=f"{i+1}"
    )
    
    db.add(new_blog)
    db.commit()

test_function()

# 使用 SQL 語法 query
def test2_function():
  with engine.connect() as con:
    statement = text("""SELECT * FROM blogs""")

    all_data = con.execute(statement).fetchall()

    for row in all_data:
      for key, value in row.items():
        print(key, value)

# test2_function()