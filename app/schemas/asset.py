from typing import Optional
from pydantic import BaseModel

class AssetCreate(BaseModel):
    name: str
    tags: Optional[list[str]] = None

class AssetRead(AssetCreate):
    id: int
    file_name: Optional[str] = None

    class Config:
        from_attributes = True