from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Neighborhood(Base):
    __tablename__ = "neighborhoods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    coordinates_id = Column(Integer, ForeignKey("coordinates.id"), nullable=False)
    score = Column(Float)
    avg_price = Column(Integer)  # calculated from neighborhood_rent

    coordinates = relationship("Coordinates")

    amenities = relationship("Amenity", back_populates="neighborhood", cascade="all, delete-orphan")

    neighborhood_rents = relationship("NeighborhoodRent", back_populates="neighborhood", cascade="all, delete")
