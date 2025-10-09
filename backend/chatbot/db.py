from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Change this as per your MySQL credentials
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/gemini_chat"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
