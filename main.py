from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uv

app = FastAPI()

class Blog(BaseModel):
    title: str
    content : str
    published : Optional[bool]



@app.get("/get-blog")
def get_blog(limit = 10, published: bool = True, sort : Optional[bool] = None):
    return {"data": f"{limit} blogs from the list, where published equals {published}"}


@app.post("/create-blog")
def create_blog(blog: Blog):
    return {"data": f"The blog is published with the title {blog.title}"}

if __name__ == "__main__":
    uvicorn.run
