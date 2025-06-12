from fastapi import FastAPI

from openapi.api.routers.auth import router as auth_router

app = FastAPI(
    title="Bildmind Public API",
    description="API для відкритого модуля навчання платформи Bildmind.",
    version="0.1.0",
    servers=[{"url": "http://localhost:8000", "description": "Локальний сервер розробки"}],
    license_info={
        "name": "CC BY-NC-ND 4.0",
        "url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
    },
)

# Підключаєш тільки те, що реалізовано
app.include_router(auth_router)


@app.get("/openapi")
def open_root():
    return {"message": "Публічний інтерфейс"}
