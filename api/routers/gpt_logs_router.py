from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.gpt_logs_crud import GPTLogCRUD
from openapi.db.schemas.gpt_logs import GptLogsCreate, GptLogsRead, GptLogsUpdate

router = APIRouter(prefix="/gpt_logs", tags=["GptLogs"])


@router.get("/", response_model=List[GptLogsRead])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return GPTLogCRUD.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=GptLogsRead)
def create(
    obj_in: GptLogsCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return GPTLogCRUD.create(db, obj_in)


@router.get("/{id}", response_model=GptLogsRead)
def read_one(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = GPTLogCRUD.get(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{id}", response_model=GptLogsRead)
def update(
    id: str,
    obj_in: GptLogsUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = GPTLogCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return GPTLogCRUD.update(db, db_obj, obj_in)


@router.delete("/{id}", response_model=GptLogsRead)
def delete(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_obj = GPTLogCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return GPTLogCRUD.delete(db, db_obj)
