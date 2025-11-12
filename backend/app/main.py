from fastapi import FastAPI, HTTPException
from sqlalchemy import select, insert, update, delete
from .db import engine, metadata
from .models import skills

app = FastAPI()

# Create tables if not exist
metadata.create_all(engine)

@app.get("/")
def home():
    return {"message": "SkillStack backend running!"}

# Add new skill
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

# Get all skills
@app.get("/skills/")
def get_skills():
    with engine.connect() as conn:
        result = conn.execute(select(skills)).fetchall()
        return [dict(row._mapping) for row in result]

# Update a skill
@app.put("/skills/{skill_id}")
def update_skill(skill_id: int, progress: str = None, notes: str = None, hours_spent: float = None):
    with engine.connect() as conn:
        update_data = {}
        if progress is not None:
            update_data["progress"] = progress
        if notes is not None:
            update_data["notes"] = notes
        if hours_spent is not None:
            update_data["hours_spent"] = hours_spent

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        result = conn.execute(update(skills).where(skills.c.id == skill_id).values(**update_data))
        conn.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Skill not found")
        return {"message": "Skill updated", "changes": update_data}

# Delete a skill
@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int):
    with engine.connect() as conn:
        result = conn.execute(delete(skills).where(skills.c.id == skill_id))
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Skill not found")
        return {"message": f"Skill with ID {skill_id} deleted"}

# Search skills by name
@app.get("/skills/search")
def search_skills(name: str):
    with engine.connect() as conn:
        result = conn.execute(select(skills).where(skills.c.skill_name.ilike(f"%{name}%"))).fetchall()
        return [dict(row._mapping) for row in result]
