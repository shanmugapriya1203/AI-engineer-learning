from fastapi import FastAPI,HTTPException
from pydantic import BaseModel


app=FastAPI()
class Note(BaseModel):
    title:str
    content:str


notes=[]

@app.get("/")
def home():
    return {"message":"This is home"}


@app.post("/notes")
def add_notes(note:Note):
    notes.append(note)
    return note

@app.get("/notes")
def all_notes():
    return notes

@app.get("/notes/{note_id}")
def get_note(note_id:int):
    if note_id < 0 or note_id >=len(notes):
        raise HTTPException(status_code=404 , detail="Detail Not found")
    return notes[note_id]


@app.delete("/notes/{note_id}")
def delete_note(note_id:int):
    if note_id < 0 or note_id >=len(notes):
        raise HTTPException(status_code=404,detail="note not found")
    return notes.pop(note_id)

@app.get("/search")
def search_note(q:str):
    return [n for n in notes if q.lower in n.title.lower()]