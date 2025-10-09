from sqlalchemy import create_engine
from backend.chatbot.models import Base  # Adjust path if needed

# Corrected URL: encoded @ as %40
DATABASE_URL = "mysql+pymysql://root:Admin%401234@localhost/chatbot_db"

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")
