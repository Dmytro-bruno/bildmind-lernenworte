from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.services.test_session_service import TestSessionService
from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.test_session_crud import TestSessionCRUD
from openapi.db.models.user import User
from openapi.db.schemas.test_session import TestSessionCreate, TestSessionRead, TestSessionUpdate

router = APIRouter(
    prefix="/test-sessions",
    tags=["Test Sessions"],
    responses={404: {"description": "Not found"}},
)

# === CRUD-ендпоїнти ===


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
    return TestSessionCRUD.create(db, user_id=current_user.id, obj_in=data)


@router.get(
    "/{session_id}", response_model=TestSessionRead, summary="Отримати сесію тестування за id"
)
def get_test_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TestSessionCRUD.get(db, session_id=session_id, user_id=current_user.id)


@router.get(
    "", response_model=List[TestSessionRead], summary="Отримати всі сесії тестування користувача"
)
def list_test_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TestSessionCRUD.get_all(db, user_id=current_user.id)


@router.patch("/{session_id}", response_model=TestSessionRead, summary="Оновити сесію тестування")
def update_test_session(
    session_id: UUID,
    data: TestSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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
    TestSessionCRUD.soft_delete(db, session_id=session_id, user_id=current_user.id)
    return None


# === Бізнес-ендпоїнти для інтеграції з фронтом ===


@router.post(
    "/start",
    response_model=List[dict],
    summary="Старт тест-сесії (10 пар слів для тесту)",
)
def start_test_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TestSessionService.start_test_session(db, current_user.id)


@router.post(
    "/answer",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Відправити відповідь по слову",
)
def answer_word(
    word_id: UUID,
    is_correct: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        TestSessionService.process_answer(
            db=db,
            user_id=current_user.id,
            word_id=word_id,
            is_correct=is_correct,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return


@router.post(
    "/finish",
    response_model=TestSessionRead,
    summary="Завершити тест-сесію та записати результат",
)
def finish_test_session(
    start_time: datetime,
    end_time: datetime,
    words_total: int,  # !!! Поля називаються ТАК, як у схемі
    correct: int,
    test_type: str = "default",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TestSessionService.finish_test_session(
        db=db,
        user_id=current_user.id,
        start_time=start_time,
        end_time=end_time,
        words_total=words_total,
        correct=correct,
        test_type=test_type,
    )
