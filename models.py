from sqlalchemy import Column, Integer, String
from database import Base

class ApiBot(Base):
    __tablename__ = 'apibot'
    id = Column(Integer, primary_key=True)
    apikey = Column(String(255))
    image = Column(String(255))
    color = Column(String(255))
    textcolor = Column(String(255))
    title = Column(String(255))
    initial = Column(String(255))