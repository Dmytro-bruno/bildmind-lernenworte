from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from openapi.api.routers.auth import router as auth_router
from openapi.api.routers.daily_progress_router import router as daily_progress_router
from openapi.api.routers.gpt_logs_router import router as gpt_logs_router
from openapi.api.routers.health import router as health
from openapi.api.routers.level_progress_router import router as level_progress_router
from openapi.api.routers.ping import router as ping_router
from openapi.api.routers.test_session_router import router as test_session_router
from openapi.api.routers.token_blacklist_router import router as token_blacklist_router
from openapi.api.routers.user_router import router as user_router
from openapi.api.routers.user_settings_router import router as user_settings_router
from openapi.api.routers.user_stats_router import router as user_stats_router
from openapi.api.routers.user_word_router import router as user_word_router
from openapi.api.routers.word_router import router as word_router

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

# Додай CORS підтримку одразу після створення app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:8082",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://10.0.2.2:8080",  # ✅ Додай це
        "http://10.0.2.2:5173",  # ✅ І це (якщо фронт працює на цьому порту)
        "capacitor://localhost",
        "https://localhost",
    ],  # 👈 дозволяє фронтенду
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключаєш тільки те, що реалізовано
app.include_router(auth_router)
app.include_router(daily_progress_router)
app.include_router(gpt_logs_router)
app.include_router(level_progress_router)
app.include_router(test_session_router)
app.include_router(token_blacklist_router)
app.include_router(user_router)
app.include_router(user_settings_router)
app.include_router(user_stats_router)
app.include_router(user_word_router)
app.include_router(word_router)
app.include_router(health)
app.include_router(ping_router)


@app.get("/openapi")
def open_root():
    return {"message": "Публічний інтерфейс"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "openapi.main:app",
        host="0.0.0.0",  # nosec B104
        port=8000,
        ssl_keyfile="ssl/key.pem",
        ssl_certfile="ssl/cert.pem",
        reload=True,
    )
