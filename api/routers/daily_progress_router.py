from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.daily_progress_crud import DailyProgressCRUD
from openapi.db.schemas.daily_progress import (
    DailyProgressCreate,
    DailyProgressRead,
    DailyProgressUpdate,
)

router = APIRouter(prefix="/daily_progresss", tags=["DailyProgress"])


@router.get("/", response_model=List[DailyProgressRead])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return DailyProgressCRUD.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=DailyProgressRead)
def create(
    obj_in: DailyProgressCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return DailyProgressCRUD.create(db, obj_in)


@router.get("/{id}", response_model=DailyProgressRead)
def read_one(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = DailyProgressCRUD.get(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{id}", response_model=DailyProgressRead)
def update(
    id: str,
    obj_in: DailyProgressUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = DailyProgressCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return DailyProgressCRUD.update(db, db_obj, obj_in)


@router.delete("/{id}", response_model=DailyProgressRead)
def delete(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_obj = DailyProgressCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return DailyProgressCRUD.delete(db, db_obj)
