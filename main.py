from database import engine, SessionLocal
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
import models


SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


class User(BaseModel):
    username: str
    name: str
    email_id: str
    liked_blogs: str | None = None


class UserInDB(User):
    hashed_password: str


class Blog(BaseModel):
    user_id: str | None = None
    blog_title: str
    blog_summary: str
    blog_content: str
    likes: str | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    print(db)
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/get_current_user/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/", tags=["BlogOn"])
def root():
    return {"message": "Hello World"}


@app.get("/users", tags=["User"])
def get_users(db: db_dependency):
    users = db.query(models.User).all()
    return [User(**user.__dict__) for user in users]


@app.get("/users/{user_id}", tags=["User"])
def get_users(db: db_dependency, user_id: int):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return User(**user.__dict__)


@app.get("/users/{username}", tags=["User"])
def get_users(db: db_dependency, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return User(**user.__dict__)


@app.get("/blogs", tags=["Blog"])
def get_blogs(db: db_dependency):
    return db.query(models.Blog).all()


@app.get("/blogs/{blog_id}", tags=["Blog"])
def get_blog(db: db_dependency, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()


@app.get("/blogs_by_user/{username}", tags=["Blog"])
def get_blogs_by_user(db: db_dependency, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return db.query(models.Blog).filter(models.Blog.user_id == user.user_id).all()


@app.post("/like")
def like(db: db_dependency, user_id: int, blog_id: int):
    db_blog = db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    liked_blogs = db_user.data_list
    likes = db_blog.data_list
    if str(blog_id) not in liked_blogs and str(user_id) not in likes:
        liked_blogs.append(str(blog_id))
        likes.append(str(user_id))
        db_blog.data_list = likes
        db_user.data_list = liked_blogs
        db.commit()
        return f"Blog {blog_id} is liked by user {user_id}"
    else:
        return f"Blog {blog_id} is already liked by user {user_id}"


@app.post("/add_user", tags=["User"])
def add_user(user: UserInDB, db: db_dependency):
    user.hashed_password = get_password_hash(user.hashed_password)
    db_user = models.User(**user.__dict__)

    db.add(db_user)
    db.commit()
    return "User added successfully"


@app.post("/add_blog", tags=["Blog"])
def add_Blog(
    blog: Blog, db: db_dependency, current_user: User = Depends(get_current_active_user)
):
    blog.user_id = current_user.user_id
    db_blog = models.Blog(**blog.__dict__)
    db.add(db_blog)
    db.commit()
    return "Blog added successfully"


# delete & update should be updated


@app.post("/delete_user", tags=["User"])
def delete_user(user_id, db: db_dependency):
    db.query(models.User).filter(models.User.user_id == user_id).delete()
    db.commit()
    return "User deleted successfully"


@app.post("/delete_blog", tags=["Blog"])
def delete_Blog(
    blog_id, db: db_dependency, current_user: User = Depends(get_current_active_user)
):
    blog = db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()
    if blog.user_id == current_user.user_id:
        db.query(models.Blog).filter(models.Blog.blog_id == blog_id).delete()
        db.commit()
        return "Blog deleted successfully"
    return "You are not authenticated"


import json, requests


@app.post("/generate_fake_users")
def generate_fake_users(lst: str):
    lst = json.loads(lst)
    for user in lst:
        response = requests.post("http://127.0.0.1:8000/add_user", json=user)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Error adding user"),
            )
    return "Completed"


@app.post("/generate_fake_blogs")
def generate_fake_blogs(lst: str):
    lst = json.loads(lst)
    for blog in lst:
        response = requests.post("http://127.0.0.1:8000/add_blog", json=blog)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Error adding blog"),
            )
    return "Completed"
