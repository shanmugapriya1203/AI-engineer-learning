from fastapi import FastAPI,HTTPException
from pydantic import BaseModel


app=FastAPI()
class Note(BaseModel):
    title:str
    content:str


notes={}
next_id=1

@app.get("/")
def home():
    return {"message":"This is home"}


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