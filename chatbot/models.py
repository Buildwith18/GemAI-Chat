# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime

# Base = declarative_base()

# class ChatHistory(Base):
#     __tablename__ = "chat_history"

#     id = Column(Integer, primary_key=True, index=True)
#     prompt = Column(String(2048))
#     response = Column(String(4096))
#     model = Column(String(50))
#     timestamp = Column(DateTime, default=datetime.utcnow)
