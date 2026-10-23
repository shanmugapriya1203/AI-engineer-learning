import os
from datetime import datetime,timedelta,timezone

import bcrypt
import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

SECRET_KEY=os.getenv("SECRET_KEY","dev-secret-change-me")
ALGORITHM='HS256'
TOKEN_MINUTES=30


app=FastAPI()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
class Note(BaseModel):
    title:str
    content:str

class UserIn(BaseModel):
    username:str=Field(min_length=3)
    password:str=Field(min_length=8,max_length=72)

users={}
notes={}
next_id=1

def hash_password(password:str)->str:
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

def verify_password(password:str, hashed:str)->bool:
    return bcrypt.checkpw(password.encode(),hashed.encode())

def create_token(username:str)->str:
    expire=datetime.now(timezone.utc)+ timedelta(minutes=TOKEN_MINUTES)
    return jwt.encode({"sub":username,"exp":expire},SECRET_KEY,algorithms=ALGORITHM)

def get_current_user(token:str=Depends(oauth2_scheme))->str:
    error=HTTPException(
        status_code=401,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise error
    username=payload.get("sub")
    if username not in users:
        raise error
    return username
@app.get("/")
def home():
    return {"message":"This is home"}

@app.post("/register",status_code=201)
def register(user:UserIn):
    if user.username in users:
        raise HTTPException(status_code=409,detail="Username already exists")
    users[user.username]=hash_password(user.password)
    return{"message":"User created","username":user.username}


@app.post("/notes",status_code=201)
def add_notes(note:Note):
    global next_id
    new_id=next_id
    notes[new_id]=note
    next_id+=1
    return {"id":new_id, "note":note}
    

@app.get("/notes")
def list_notes(q:str | None= None ,limit:int=10):
    result=[{"id":i,'note':n} for i ,n in notes.items()]
    if q:
        result=[r for r in result if q.lower() in r[note].title.lower()]
    return result[:limit]

@app.get("/notes/{note_id}")
def get_note(note_id:int):
    if note_id < 0 or note_id >=len(notes):
        raise HTTPException(status_code=404 , detail="Detail Not found")
    return notes[note_id]

@app.put("/notes/{note_id}")
def update_note(note_id:int,note:Note):
    if note_id not in notes:
        raise HTTPException(status_code=404,detail="Message not found")
    notes[note_id]=note
    return [{"id":note_id,"note":note}]



@app.delete("/notes/{note_id}")
def delete_note(note_id:int):
    if note_id < 0 or note_id >=len(notes):
        raise HTTPException(status_code=404,detail="note not found")
    return notes.pop(note_id)

@app.get("/search")
def search_note(q:str):
    return [n for n in notes if q.lower in n.title.lower()]