from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Smart ToDo API")

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set")

client = MongoClient(MONGO_URI)
client.server_info()

db = client["smart_todo_db"]
users_collection = db["users"]
tasks_collection = db["tasks"]

SECRET_KEY = "smarttodo_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    payload = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


class UserRegister(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskResponse(TaskCreate):
    id: str


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        user = users_collection.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


@app.post("/register")
def register_user(user: UserRegister):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="User already exists")

    users_collection.insert_one({
        "username": user.username,
        "password": hash_password(user.password)
    })

    return {"message": "User registered successfully"}


@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": form_data.username})

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"sub": user["username"]},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": token, "token_type": "bearer"}


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, current_user=Depends(get_current_user)):
    result = tasks_collection.insert_one({
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "owner": current_user["username"]
    })
    return {**task.dict(), "id": str(result.inserted_id)}


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(current_user=Depends(get_current_user)):
    tasks = []
    for task in tasks_collection.find({"owner": current_user["username"]}):
        tasks.append({
            "id": str(task["_id"]),
            "title": task["title"],
            "description": task.get("description"),
            "completed": task["completed"]
        })
    return tasks


@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: TaskCreate, current_user=Depends(get_current_user)):
    result = tasks_collection.update_one(
        {"_id": ObjectId(task_id), "owner": current_user["username"]},
        {"$set": task.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task updated successfully"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, current_user=Depends(get_current_user)):
    result = tasks_collection.delete_one(
        {"_id": ObjectId(task_id), "owner": current_user["username"]}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}
