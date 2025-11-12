from fastapi import FastAPI
from .db import engine, metadata
from .models import skills


app = FastAPI()
@app.get("/")
def home():
    return {"message": "SkillStack Backend is running!"}