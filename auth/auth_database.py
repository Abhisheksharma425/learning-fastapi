from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 'sqlite:///filename.db' defines a local file database
# Use 'sqlite:///:memory:' for a temporary database in RAM
engine = create_engine('sqlite:///my_database.db', echo=True)

##Session

SessionLocal = sessionmaker(autoflush= False, autocommit = False, bind= engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


##Base

Base = declarative_base()


