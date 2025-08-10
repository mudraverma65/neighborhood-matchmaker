from database import Base
from sqlalchemy import Column, Integer, Float

class Coordinates(Base):
    __tablename__ = "coordinates"
    id = Column(Integer, index = True, autoincrement= True, primary_key=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
