from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.test_session_crud import TestSessionCRUD
from openapi.db.models.user import User
from openapi.db.schemas.test_session import TestSessionCreate, TestSessionRead, TestSessionUpdate

router = APIRouter(
    prefix="/test-sessions",
    tags=["Test Sessions"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=TestSessionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Створити сесію тестування",
)
def create_test_session(
    data: TestSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Додає нову сесію тестування для поточного користувача.
    """
    return TestSessionCRUD.create(db, user_id=current_user.id, obj_in=data)


@router.get(
    "/{session_id}", response_model=TestSessionRead, summary="Отримати сесію тестування за id"
)
def get_test_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає конкретну сесію тестування поточного користувача.
    """
    return TestSessionCRUD.get(db, session_id=session_id, user_id=current_user.id)


@router.get(
    "", response_model=List[TestSessionRead], summary="Отримати всі сесії тестування користувача"
)
def list_test_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає список усіх активних сесій тестування користувача.
    """
    return TestSessionCRUD.get_all(db, user_id=current_user.id)


@router.patch("/{session_id}", response_model=TestSessionRead, summary="Оновити сесію тестування")
def update_test_session(
    session_id: UUID,
    data: TestSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює сесію тестування (partial update).
    """
    return TestSessionCRUD.update(db, session_id=session_id, user_id=current_user.id, obj_in=data)


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити сесію тестування (soft-delete)",
)
def delete_test_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    М'яко видаляє сесію тестування (ставить deleted_at).
    """
    TestSessionCRUD.soft_delete(db, session_id=session_id, user_id=current_user.id)
    return None
