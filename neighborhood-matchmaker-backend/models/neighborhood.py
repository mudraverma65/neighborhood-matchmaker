from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Many-to-many association table
neighborhood_amenities = Table(
    "neighborhood_amenities",
    Base.metadata,
    Column("neighborhood_id", Integer, ForeignKey("neighborhoods.id")),
    Column("amenity_id", Integer, ForeignKey("amenities.id"))
)

class Neighborhood(Base):
    __tablename__ = "neighborhoods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    coordinates_id = Column(Integer, ForeignKey("coordinates.id"), nullable=False)
    score = Column(Float)
    avg_price = Column(Integer)

    coordinates = relationship("Coordinates")
    amenities = relationship("Amenity", secondary=neighborhood_amenities, back_populates="neighborhoods")
