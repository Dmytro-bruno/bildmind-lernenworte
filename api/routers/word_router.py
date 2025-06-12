from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.word_crud import WordCRUD
from openapi.db.models.user import User
from openapi.db.schemas.word import WordCreate, WordRead, WordUpdate

router = APIRouter(
    prefix="/words",
    tags=["Words"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=WordRead,
    status_code=status.HTTP_201_CREATED,
    summary="Додати слово у словник",
)
def create_word(
    data: WordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Додає нове слово до загального словника.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Дозволено лише адміну")
    return WordCRUD.create(db, obj_in=data)


@router.get("", response_model=List[WordRead], summary="Отримати всі слова із словника")
def list_words(
    skip: int = Query(0, ge=0, description="Пропустити N записів"),
    limit: int = Query(100, ge=1, le=1000, description="Скільки записів повернути"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Повертає всі не видалені слова (можна фільтрувати через skip/limit).
    """
    return WordCRUD.get_all(db, skip=skip, limit=limit)


@router.get("/{word_id}", response_model=WordRead, summary="Отримати слово за id")
def get_word(
    word_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Повертає слово по id.
    """
    word = WordCRUD.get_by_id(db, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Слово не знайдено")
    return word


@router.patch("/{word_id}", response_model=WordRead, summary="Оновити слово у словнику")
def update_word(
    word_id: UUID,
    data: WordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює слово у словнику (тільки адмін).
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Дозволено лише адміну")
    return WordCRUD.update(db, word_id=word_id, obj_in=data)


@router.delete(
    "/{word_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити слово зі словника (soft-delete)",
)
def delete_word(
    word_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    М'яко видаляє слово зі словника (тільки адмін).
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Дозволено лише адміну")
    WordCRUD.soft_delete(db, word_id=word_id)
    return None
