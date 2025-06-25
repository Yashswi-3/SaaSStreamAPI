from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(
    title="SaaS News API Pipeline",
    version="0.1.0",
    description="API for scraping, processing, and serving SaaS news articles."
)
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the SaaS News API Pipeline"}
