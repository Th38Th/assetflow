import os
import shutil

from fastapi import UploadFile
from sqlalchemy import String

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetRead
from app.schemas.user import UserInDB
from sqlalchemy.orm import Session

UPLOAD_DIR = "uploaded_assets"

def upload_file(file: UploadFile):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file.filename

def get_file_info(file_name: String) -> tuple[str, str]:
    return (file_name, os.path.join(UPLOAD_DIR, file_name))

def create_asset(db: Session, asset: AssetCreate, user: UserInDB):
    new_asset = Asset(**asset.model_dump(), owner_id=user.id)
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset

def get_asset(db: Session, asset_id: int, user: UserInDB):
    return db.query(Asset).filter(Asset.id == asset_id, Asset.owner_id == user.id).first()

def delete_asset(db: Session, asset_id: int, user: UserInDB) -> bool:
    asset = get_asset(db, asset_id, user)
    if not asset:
        return False
    db.delete(asset)
    db.commit()
    return True

def update_asset(db: Session, asset_id: int, asset_data: AssetCreate, user: UserInDB):
    asset = get_asset(db, asset_id, user)
    if not asset:
        return None
    asset.name = asset_data.name
    asset.tags = asset_data.tags
    db.commit()
    db.refresh(asset)
    return asset

def get_asset_file(db: Session, asset_id: int, user: UserInDB) -> tuple[str, str]:
    asset = get_asset(db, asset_id, user)
    file_name = asset.file_name
    file_path = get_file_info(file_name)
    return file_path

def get_assets(db: Session, user: UserInDB):
    return db.query(Asset).filter(Asset.owner_id == user.id).all()

def update_tags(db: Session, asset_id: int, user: UserInDB, tags: list[str]):
    asset = get_asset(db, asset_id, user)
    if not asset:
        return None
    asset.tags = tags
    db.commit()
    db.refresh(asset)
    return asset

def upload_asset_file(db: Session, asset_id: int, user: UserInDB, file: UploadFile):
    asset = get_asset(db, asset_id, user)
    if not asset:
        return None
    asset_filename = upload_file(file)
    asset.file_name = asset_filename
    db.commit()
    db.refresh(asset)
    return asset