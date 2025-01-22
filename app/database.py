from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

# Declarative Base
Base = declarative_base()
# Database URL
DATABASE_URL = "sqlite:///./app.db"

# SQLAlchemy Engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create the tables
Base.metadata.create_all(engine)

# SessionLocal for Dependency Injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to Get Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
