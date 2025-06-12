from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.gpt_logs_crud import GPTLogsCRUD
from openapi.db.models.user import User
from openapi.db.schemas.gpt_logs import GPTLogCreate, GPTLogRead, GPTLogUpdate

router = APIRouter(
    prefix="/gpt-logs",
    tags=["GPT Logs"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=GPTLogRead,
    status_code=status.HTTP_201_CREATED,
    summary="Створити log GPT-запиту",
)
def create_gpt_log(
    data: GPTLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Додає новий log GPT для поточного користувача.
    """
    return GPTLogsCRUD.create(db, user_id=current_user.id, obj_in=data)


@router.get("/{log_id}", response_model=GPTLogRead, summary="Отримати log за id")
def get_gpt_log(
    log_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає конкретний log GPT поточного користувача.
    """
    return GPTLogsCRUD.get(db, log_id=log_id, user_id=current_user.id)


@router.get("", response_model=List[GPTLogRead], summary="Отримати всі логи поточного користувача")
def list_gpt_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає список усіх логів GPT користувача (від нових до старих).
    """
    return GPTLogsCRUD.get_all(db, user_id=current_user.id)


@router.patch("/{log_id}", response_model=GPTLogRead, summary="Оновити log GPT (partial update)")
def update_gpt_log(
    log_id: UUID,
    data: GPTLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює log GPT (доступно тільки автору).
    """
    return GPTLogsCRUD.update(db, log_id=log_id, user_id=current_user.id, obj_in=data)


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Видалити log GPT")
def delete_gpt_log(
    log_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Видаляє log GPT поточного користувача.
    """
    GPTLogsCRUD.delete(db, log_id=log_id, user_id=current_user.id)
    return None
