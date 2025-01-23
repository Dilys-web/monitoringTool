from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from app.database import Base

engine = create_engine('sqlite:///app.db')  # replace with your database URL

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class AWSCredentials(Base):
    __tablename__ = "aws_credentials"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    aws_access_key = Column(String)
    aws_secret_key = Column(String)

    user = relationship("User", backref="aws_credentials")


try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(f"Error creating tables: {e}")