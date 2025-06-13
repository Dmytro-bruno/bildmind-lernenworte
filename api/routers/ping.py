from fastapi import APIRouter

router = APIRouter(tags=["Monitoring"])


@router.get("/ping", summary="Перевірка чи живий API")
async def ping():
    return {"ping": "pong"}
