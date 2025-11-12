from fastapi import FastAPI
from sqlalchemy import select, insert
from .db import engine, metadata
from .models import skills

app = FastAPI()

# ✅ Create all tables in the database (if not created yet)
metadata.create_all(engine)

@app.get("/")
def home():
    return {"message": "SkillStack backend running!"}

# ✅ Add a new skill
@app.post("/skills/")
def add_skill(skill_name: str, resource_type: str = None, platform: str = None):
    with engine.connect() as conn:
        new_skill = {
            "skill_name": skill_name,
            "resource_type": resource_type,
            "platform": platform,
            "progress": "started",
            "hours_spent": 0,
            "notes": "",
            "difficulty_rating": 3
        }
        conn.execute(insert(skills).values(**new_skill))
        conn.commit()
        return {"message": "Skill added successfully", "skill": new_skill}

# ✅ Get all skills
@app.get("/skills/")
def get_skills():
    with engine.connect() as conn:
        result = conn.execute(select(skills)).fetchall()
        return [dict(row._mapping) for row in result]
