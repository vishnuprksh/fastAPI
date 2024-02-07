from fastapi import FastAPI
from . import schemas, models
from .database import engine

app = FastAPI()
models.Base.metadata.create_all(engine)

@app.post("/blog")
def create(request: schemas.Blog):
    return {f"blog with title {request.title} and body {request.body}"}


