from sqlalchemy.orm import Session

from openapi.db.models.test_session import TestSession


class TestSessionCRUD:
    @staticmethod
    def get(db: Session, id):
        return db.query(TestSession).filter(TestSession.id == id).first()

    @staticmethod
    def get_all(db: Session, skip=0, limit=100):
        return db.query(TestSession).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, obj_in):
        db_obj = TestSession(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db: Session, db_obj, obj_in):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, db_obj):
        db.delete(db_obj)
        db.commit()
        return db_obj
