from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHAMY_DATABASE_URL = 'sqlite:///./blog/blog.db'

# engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={ "check_same_thread": False })
engine = create_engine('postgresql://localhost:5431/wilson')

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# ----- function -------------------------------------------------------------------------------------------------------------------------

def get_db():
  db = SessionLocal()
  print(SessionLocal())
  
  try:
    yield db
  finally:
    db.close()