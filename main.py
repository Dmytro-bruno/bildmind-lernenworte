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

app = FastAPI(title="Bildmind Public API")

# Підключаємо всі роутери
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
