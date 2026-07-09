from fastapi import APIRouter, Depends, Request, status, BackgroundTasks
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserLoginSchema, UserSchema, UserResponseSchema, LoginResponseSchema
from . import controller

user_router = APIRouter(prefix="/user")


@user_router.post("/register", response_model= UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(body: UserSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return await controller.register(body, db, background_tasks)


@user_router.post("/login", response_model=LoginResponseSchema, status_code=status.HTTP_200_OK)
def login_user(body: UserLoginSchema, db: Session = Depends(get_db)):
    return controller.login(body, db)

@user_router.get("/is_auth", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def is_auth(request: Request, db: Session = Depends(get_db)):
    return controller.is_auth(request, db)