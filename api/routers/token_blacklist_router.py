from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.token_blacklist_crud import TokenBlacklistCRUD
from openapi.db.schemas.token_blacklist import (
    TokenBlacklistCreate,
    TokenBlacklistRead,
    TokenBlacklistUpdate,
)

router = APIRouter(prefix="/token_blacklists", tags=["TokenBlacklist"])


@router.get("/", response_model=List[TokenBlacklistRead])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return TokenBlacklistCRUD.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=TokenBlacklistRead)
def create(
    obj_in: TokenBlacklistCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return TokenBlacklistCRUD.create(db, obj_in)


@router.get("/{id}", response_model=TokenBlacklistRead)
def read_one(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = TokenBlacklistCRUD.get(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{id}", response_model=TokenBlacklistRead)
def update(
    id: str,
    obj_in: TokenBlacklistUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = TokenBlacklistCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return TokenBlacklistCRUD.update(db, db_obj, obj_in)


@router.delete("/{id}", response_model=TokenBlacklistRead)
def delete(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_obj = TokenBlacklistCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return TokenBlacklistCRUD.delete(db, db_obj)
