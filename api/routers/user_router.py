from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.user_crud import UserCRUD
from openapi.db.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/", response_model=List[UserRead])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return UserCRUD.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=UserRead)
def create(
    obj_in: UserCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return UserCRUD.create(db, obj_in)


@router.get("/{id}", response_model=UserRead)
def read_one(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = UserCRUD.get(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{id}", response_model=UserRead)
def update(
    id: str,
    obj_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = UserCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return UserCRUD.update(db, db_obj, obj_in)


@router.delete("/{id}", response_model=UserRead)
def delete(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_obj = UserCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return UserCRUD.delete(db, db_obj)
