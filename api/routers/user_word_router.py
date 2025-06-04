from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.user_word_crud import UserWordCRUD
from openapi.db.schemas.user_word import UserWordCreate, UserWordRead, UserWordUpdate

router = APIRouter(prefix="/user_words", tags=["UserWord"])


@router.get("/", response_model=List[UserWordRead])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return UserWordCRUD.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=UserWordRead)
def create(
    obj_in: UserWordCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return UserWordCRUD.create(db, obj_in)


@router.get("/{id}", response_model=UserWordRead)
def read_one(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = UserWordCRUD.get(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{id}", response_model=UserWordRead)
def update(
    id: str,
    obj_in: UserWordUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = UserWordCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return UserWordCRUD.update(db, db_obj, obj_in)


@router.delete("/{id}", response_model=UserWordRead)
def delete(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_obj = UserWordCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return UserWordCRUD.delete(db, db_obj)
