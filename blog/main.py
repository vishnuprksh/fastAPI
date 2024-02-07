from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from  typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog",  status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog) #what is the reason to refresh here?
    return new_blog


@app.get("/blog", response_model=List[schemas.ShowBlog])
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model = schemas.ShowBlog)
def show(id, response : Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The blog not found")
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, response : Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The blog not found")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return {"response": "blog deleted"}


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The blog not found")   
    
    blog.update({models.Blog.title :request.title, models.Blog.body: request.body}, synchronize_session=False)
    db.commit()
    return {"Response": f"The blog with id {id} is updated"}


@app.post("/user")
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name =  request.name, email =  request.email, password =  request.password)
    db.add(new_user)
    db.commit()
    db.refresh()
    return new_user


