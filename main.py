from fastapi import FastAPI

from openapi.api.routers import (
    daily_progress_router,
    gpt_logs_router,
    health,
    level_progress_router,
    test_session_router,
    token_blacklist_router,
    user_router,
    user_settings_router,
    user_stats_router,
    user_word_router,
    word_router,
)

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

# Підключення роутерів
app.include_router(health.router)
app.include_router(daily_progress_router.router)
app.include_router(gpt_logs_router.router)
app.include_router(level_progress_router.router)
app.include_router(test_session_router.router)
app.include_router(token_blacklist_router.router)
app.include_router(user_router.router)
app.include_router(user_settings_router.router)
app.include_router(user_stats_router.router)
app.include_router(user_word_router.router)
app.include_router(word_router.router)


@app.get("/openapi")
def open_root():
    return {"message": "Публічний інтерфейс"}
