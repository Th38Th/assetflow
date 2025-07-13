from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import ARRAY, String
from sqlalchemy.orm import Session
from typing import List
import mimetypes

from app.db.session import get_db
from app.schemas.asset import AssetCreate, AssetRead
from app.models.asset import Asset
from app.core.security import get_current_user
from app.schemas.user import UserInDB
from app.schemas.message import Messsage
from app.services.assets import create_asset, \
    delete_asset, get_asset, get_asset_file, \
        get_assets, update_asset, update_tags, upload_asset_file

router = APIRouter()

@router.post("/", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def create_asset_api(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
): return create_asset(db, asset, current_user)

@router.patch("/{asset_id}/file", response_model=AssetRead, status_code=status.HTTP_202_ACCEPTED)
def upload_asset_file_api(
    asset_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    updated_asset = upload_asset_file(db, asset_id, current_user, file)
    if not updated_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found or not accessible"
        )
    return updated_asset

@router.patch("/{asset_id}/tags", response_model=AssetRead, status_code=status.HTTP_202_ACCEPTED)
def update_tags_api(
    asset_id: int,
    tags: list[str],
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    updated_asset = update_tags(db, asset_id, current_user, tags)
    if not updated_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found or not accessible"
        )
    return updated_asset

@router.get("/", response_model=List[AssetRead])
def get_assets_api(
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
): return get_assets(db, current_user)

@router.get("/{asset_id}", response_model=AssetRead)
def get_asset_by_id(
    asset_id: int,    
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    asset = get_asset(db, asset_id, current_user)    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found or not accessible")
    return asset

@router.get("/{asset_id}/file", response_class=FileResponse)
def download_asset(
    asset_id: int,    
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    file_result = get_asset_file(db, asset_id, current_user)
    file_path = file_result[1]
    file_name = file_result[0]
    mime_type, _ = mimetypes.guess_type(file_path)
    mime_type = mime_type or "application/octet-stream"
    return FileResponse(
        path=file_path,
        media_type=mime_type,
        filename=file_name
    )

@router.delete("/{asset_id}", response_model=Messsage, status_code=200)
def delete_asset_api(
    asset_id: int,    
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    was_deleted = delete_asset(db, asset_id, current_user)
    if not was_deleted:
        raise HTTPException(status_code=404, detail="Asset not found or not accessible")
    return {
        "message": f"Item {asset_id} deleted"
    }

@router.put("/{asset_id}", response_model=AssetRead)
def update_asset_api(
    asset_id: int,
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
): 
    updated_asset = update_asset(db, asset_id, asset, current_user)
    if not updated_asset:
        raise HTTPException(status_code=404, detail="Asset not found or not accessible")
    return updated_asset