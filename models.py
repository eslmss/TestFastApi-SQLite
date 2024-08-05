from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class ItemDB(Base):
    """
    Define la estructura de la tabla en la base de datos SQLite, se utilizará para interactuar directamente con la base de datos
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

class Item(BaseModel):
    """
    Define la estructura de un objeto Item
    """
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
        
# uvicorn main:app --reload