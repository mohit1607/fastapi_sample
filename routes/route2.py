from fastapi import APIRouter, Depends, HTTPException
from connection.connection_sql import engine, SessionLocal
from sqlalchemy.orm import Session
from sql_controllers import controllers
from sql_models import models
from schemas import sql_schemas

models.Base.metadata.create_all(bind=engine)


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
        #things will happen here for every function in which it is injected.
    finally:
        db.close()


@router.post("/users/", response_model=sql_schemas.User)
def create_user(user: sql_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = controllers.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return controllers.create_user(db=db, user=user)


@router.get("/users/", response_model=list[sql_schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = controllers.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=sql_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = controllers.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/items/", response_model=sql_schemas.Item)
def create_item_for_user(
    user_id: int, item: sql_schemas.ItemCreate, db: Session = Depends(get_db)
):
    return controllers.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/", response_model=list[sql_schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = controllers.get_items(db, skip=skip, limit=limit)
    return items