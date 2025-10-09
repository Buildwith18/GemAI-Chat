from sqlalchemy import create_engine
from chatbot.models import Base  # ✅ Correct import

# Ensure password is URL-encoded (Admin@1234 => Admin%401234)
DATABASE_URL = "mysql+pymysql://root:Admin%401234@localhost/chatbot_db"

engine = create_engine(DATABASE_URL)

# This will create all tables defined under the Base in models.py
Base.metadata.create_all(bind=engine)

print("Tables created successfully.")
