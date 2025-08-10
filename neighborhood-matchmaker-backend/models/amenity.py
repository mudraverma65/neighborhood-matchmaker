from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from enums.amenity_type import AmenityTypeEnum

class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(AmenityTypeEnum), nullable=False)
    count = Column(Integer, nullable=False, default=0)

    neighborhoods = relationship("Neighborhood", secondary="neighborhood_amenities", back_populates="amenities")
