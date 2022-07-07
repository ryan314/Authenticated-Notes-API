from fastapi import FastAPI, Depends, Path, Query, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Note(BaseModel):
    date: str
    title: str 
    notes: str
    category: str

notes_library = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token') 

@app.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()): 
    return {"NOTES": notes_library}


@app.get('/gen_auth')
async def gen_auth(token: str = Depends(oauth2_scheme)): 
    return {'Authentication generation status': "Success"}


@app.post("/create_item") 
def create_note(*, note_id: int, note: Note):
    if note_id in notes_library:
        raise HTTPException(status_code = 400, detail = "Note ID already exists.")
    
    notes_library[note_id] = note
    return notes_library[note_id]


@app.get("/get_by_title")
def get_by_title(*, title: str):
    for i in notes_library:
        if notes_library[i].title == title:
            return notes_library[i]
        else:
            raise HTTPException(status_code = 401, detail = "Title does not exist.")


@app.delete("/delete_note")
def delete_note(*, title: str):
    for i in notes_library:
        if notes_library[i].title == title:
            del notes_library[i]
            return {"Success!": "Noted deleted!"}

    raise HTTPException(status_code = 401, detail = "Title does not exist.")