from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.level_progress_crud import LevelProgressCRUD
from openapi.db.schemas.level_progress import (
    LevelProgressCreate,
    LevelProgressRead,
    LevelProgressUpdate,
)

router = APIRouter(prefix="/level_progresss", tags=["LevelProgress"])


@router.get("/", response_model=List[LevelProgressRead])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return LevelProgressCRUD.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=LevelProgressRead)
def create(
    obj_in: LevelProgressCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return LevelProgressCRUD.create(db, obj_in)


@router.get("/{id}", response_model=LevelProgressRead)
def read_one(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = LevelProgressCRUD.get(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{id}", response_model=LevelProgressRead)
def update(
    id: str,
    obj_in: LevelProgressUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = LevelProgressCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return LevelProgressCRUD.update(db, db_obj, obj_in)


@router.delete("/{id}", response_model=LevelProgressRead)
def delete(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_obj = LevelProgressCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return LevelProgressCRUD.delete(db, db_obj)
