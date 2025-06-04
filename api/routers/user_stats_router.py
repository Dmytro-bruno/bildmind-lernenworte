from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.user_stats_crud import UserStatsCRUD
from openapi.db.schemas.user_stats import UserStatsCreate, UserStatsRead, UserStatsUpdate

router = APIRouter(prefix="/user_statss", tags=["UserStats"])


@router.get("/", response_model=List[UserStatsRead])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return UserStatsCRUD.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=UserStatsRead)
def create(
    obj_in: UserStatsCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return UserStatsCRUD.create(db, obj_in)


@router.get("/{id}", response_model=UserStatsRead)
def read_one(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = UserStatsCRUD.get(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{id}", response_model=UserStatsRead)
def update(
    id: str,
    obj_in: UserStatsUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = UserStatsCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return UserStatsCRUD.update(db, db_obj, obj_in)


@router.delete("/{id}", response_model=UserStatsRead)
def delete(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_obj = UserStatsCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return UserStatsCRUD.delete(db, db_obj)
