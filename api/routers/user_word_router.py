from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.services.user_word_service import UserWordService
from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.user_word_crud import UserWordCRUD
from openapi.db.models.user import User
from openapi.db.schemas.user_word import UserWordRead, UserWordUpdate
from openapi.db.schemas.word import WordCreate

router = APIRouter(
    prefix="/user-words",
    tags=["User Words"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=UserWordRead,
    status_code=status.HTTP_201_CREATED,
    summary="Додати слово у словник користувача (створює глобальне слово, якщо треба)",
)
def create_user_word(
    data: WordCreate,  # <-- Основна зміна: тут WordCreate, бо якщо слова нема — воно створюється!
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Додає нове слово до словника користувача (і створює глобальне слово, якщо треба).
    """
    return UserWordService.add_word_for_user(
        db=db,
        user_id=current_user.id,
        word_in=data,
    )


@router.get(
    "", response_model=List[UserWordRead], summary="Отримати всі слова зі словника користувача"
)
def list_user_words(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає всі слова зі словника поточного користувача.
    """
    return UserWordCRUD.get_all(db, user_id=current_user.id)


@router.get(
    "/{user_word_id}", response_model=UserWordRead, summary="Отримати слово зі словника за id"
)
def get_user_word(
    user_word_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає слово зі словника за id (user_word_id).
    """
    user_word = UserWordCRUD.get_by_id(db, user_id=current_user.id, user_word_id=user_word_id)
    if not user_word:
        raise HTTPException(status_code=404, detail="Слово не знайдено")
    return user_word


@router.patch("/{user_word_id}", response_model=UserWordRead, summary="Оновити слово зі словника")
def update_user_word(
    user_word_id: UUID,
    data: UserWordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює слово зі словника поточного користувача.
    """
    return UserWordCRUD.update(db, user_id=current_user.id, user_word_id=user_word_id, obj_in=data)


@router.delete(
    "/{user_word_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити слово зі словника (soft-delete)",
)
def delete_user_word(
    user_word_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    М'яко видаляє слово зі словника поточного користувача.
    """
    UserWordCRUD.soft_delete(db, user_id=current_user.id, user_word_id=user_word_id)
    return None
