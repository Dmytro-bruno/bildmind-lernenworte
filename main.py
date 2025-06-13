from fastapi import FastAPI

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
