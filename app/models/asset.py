from sqlalchemy import ARRAY, Column, Integer, String, Float, ForeignKey
from app.db.base import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=True)
    file_name = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
