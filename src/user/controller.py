from src.user.dtos import UserSchema, UserResponseSchema, UserLoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException, status, Request, BackgroundTasks
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime, timedelta
import jwt
from src.utils.mail import send_email

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

async def register(body: UserSchema, db: Session, background_tasks: BackgroundTasks):
    is_user_exist = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    is_user_exist = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    hashed_password = get_password_hash(body.password)
    
    new_user = UserModel(name=body.name, username=body.username, email=body.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # send email to user
    background_tasks.add_task(send_email, [new_user.email])

    return {
    "id": new_user.id,
    "name": new_user.name,
    "username": new_user.username,
    "email": new_user.email
    }

def login(body: UserLoginSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    print(f"Expiration time: {exp_time}")
    
    token = jwt.encode({"user_id": user.id, "exp": exp_time}, settings.SECRET_KEY, settings.ALGORITHM)
    
    return {"token": token}

# token send
def is_auth(request: Request, db: Session):
    token = request.headers.get("Authorization")
    print("Authorization Header:", token)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    token = token.split(" ")[1]

    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = data.get("user_id")
    exp = data.get("exp")

    current_time = datetime.now().timestamp()
    if current_time > exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="u are not authorized")

    return user 