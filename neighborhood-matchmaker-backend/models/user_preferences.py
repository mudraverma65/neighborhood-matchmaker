from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum, ARRAY
from sqlalchemy.orm import relationship
from database import Base
from .amenity_type import AmenityTypeEnum

user_pref_neighborhood = Table(
    "user_pref_neighborhood",
    Base.metadata,
    Column("user_pref_id", Integer, ForeignKey("user_preferences.id")),
    Column("neighborhood_id", Integer, ForeignKey("neighborhoods.id"))
)

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    budget = Column(Integer, nullable=False)
    max_commute_time = Column(Integer)
    email = Column(String)
    destination_id = Column(Integer, ForeignKey("coordinates.id"))
    amenities = Column(ARRAY(Enum(AmenityTypeEnum)))

    # Relationships
    destination = relationship("Coordinates")
    preferred_neighborhoods = relationship("Neighborhood", secondary=user_pref_neighborhood)
