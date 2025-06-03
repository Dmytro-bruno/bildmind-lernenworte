from fastapi import FastAPI
from api.routes import health

app = FastAPI(title="Bildmind Public API")
app.include_router(health.router)


@app.get("/open")
def open_root():
    return {"message": "Публічний інтерфейс"}
