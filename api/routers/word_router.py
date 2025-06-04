from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.word_crud import WordCRUD
from openapi.db.schemas.word import WordCreate, WordRead, WordUpdate

router = APIRouter(prefix="/words", tags=["Word"])


@router.get("/", response_model=List[WordRead])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return WordCRUD.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=WordRead)
def create(
    obj_in: WordCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return WordCRUD.create(db, obj_in)


@router.get("/{id}", response_model=WordRead)
def read_one(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = WordCRUD.get(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{id}", response_model=WordRead)
def update(
    id: str,
    obj_in: WordUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = WordCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return WordCRUD.update(db, db_obj, obj_in)


@router.delete("/{id}", response_model=WordRead)
def delete(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_obj = WordCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return WordCRUD.delete(db, db_obj)
