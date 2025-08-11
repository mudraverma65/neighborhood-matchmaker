from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Neighborhood

router = APIRouter()

@router.get("/neighborhoods")
def get_neighborhoods(db: Session = Depends(get_db)):
    neighborhoods = db.query(Neighborhood.name).all()
    names = [n[0] for n in neighborhoods]
    return names
