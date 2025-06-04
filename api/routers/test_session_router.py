from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.test_session_crud import TestSessionCRUD
from openapi.db.schemas.test_session import TestSessionCreate, TestSessionRead, TestSessionUpdate

router = APIRouter(prefix="/test_sessions", tags=["TestSession"])


@router.get("/", response_model=List[TestSessionRead])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return TestSessionCRUD.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=TestSessionRead)
def create(
    obj_in: TestSessionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return TestSessionCRUD.create(db, obj_in)


@router.get("/{id}", response_model=TestSessionRead)
def read_one(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = TestSessionCRUD.get(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{id}", response_model=TestSessionRead)
def update(
    id: str,
    obj_in: TestSessionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = TestSessionCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return TestSessionCRUD.update(db, db_obj, obj_in)


@router.delete("/{id}", response_model=TestSessionRead)
def delete(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_obj = TestSessionCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return TestSessionCRUD.delete(db, db_obj)
