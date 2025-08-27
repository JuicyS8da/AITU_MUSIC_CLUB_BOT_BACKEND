from fastapi import FastAPI
from app.users import views as user_views
from app.schedule import views as product_views

from app.common.db import init_models

app = FastAPI(title="Music Schedule Bot 6")

# Подключаем "модули" (аналог Django apps)
app.include_router(user_views.router)
app.include_router(product_views.router)

@app.on_event("startup")
async def startup_event():
    await init_models()

@app.get("/")
async def root():
    return {"message": "Welcome to My Modular FastAPI Project"}
