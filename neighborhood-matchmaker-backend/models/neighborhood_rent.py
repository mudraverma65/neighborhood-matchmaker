from database import Base
from sqlalchemy import Column, Float, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enums.rent_type import RentTypeEnum

class NeighborhoodRent(Base):
    __tablename__ = "neighborhood_rents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    neighborhood_id = Column(Integer, ForeignKey("neighborhoods.id"), nullable=False)
    type = Column(Enum(RentTypeEnum), nullable=False)
    avg_price = Column(Float, nullable=False)

    neighborhoods = relationship("Neighborhood", back_populates="neighborhood_rents", cascade="all, delete")