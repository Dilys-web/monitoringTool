from database import Base, engine
# from app.models import   # Replace with actual model names

# Create the database tables
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
