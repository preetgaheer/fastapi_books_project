from fastapi import FastAPI

from .routes.book import router as BookRouter

app = FastAPI()

app.include_router(BookRouter, tags=["Book"], prefix="/book")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}