from typing import List, Optional
from datetime import datetime, time, timedelta
from pydantic import BaseModel

class Blog(BaseModel):
  title: str
  body: str
  user_id: int

  class Config():
    orm_mode = True

class User(BaseModel):
  name: str
  email: str
  password: str

class ShowUser(BaseModel):
  name: str
  email: str
  blogs: List[Blog] = []

  class Config():
    orm_mode = True

class ShowBlog(Blog):
  creator: ShowUser

  class Config():
    orm_mode = True

class Login(BaseModel):
  username: str
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: Optional[str] = None

class Test(BaseModel):
  name: str
  title: str
  date: datetime
  number: int

class Test2(BaseModel):
  name: str
  title: str
  number: int