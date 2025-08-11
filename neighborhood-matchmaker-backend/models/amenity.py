from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from enums.amenity_type import AmenityTypeEnum


class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(AmenityTypeEnum), nullable=False)
    count = Column(Integer, nullable=False, default=0)

    neighborhood_id = Column(Integer, ForeignKey("neighborhoods.id"), nullable=False)

    # Link back to Neighborhood
    neighborhood = relationship("Neighborhood", back_populates="amenities")
