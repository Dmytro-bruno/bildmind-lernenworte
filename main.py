from api.routes import health
from fastapi import FastAPI

app = FastAPI(title="Bildmind Public API")
app.include_router(health.router)


@app.get("/openapi")
def open_root():
    return {"message": "Публічний інтерфейс"}
