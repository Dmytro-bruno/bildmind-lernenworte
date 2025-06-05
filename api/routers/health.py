from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from openapi.db.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/healthcheck")
async def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"db_status": "ok"}
    except Exception as e:
        return {"db_status": "fail", "error": str(e)}
