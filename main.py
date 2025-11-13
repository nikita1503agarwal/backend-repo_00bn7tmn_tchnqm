import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from schemas import Animal, Sighting, Volunteer, Donation
from database import create_document, get_documents, db

app = FastAPI(title="Stray Animal Welfare API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Stray Animal Welfare API is running"}

# Schema endpoint for viewers/tools
@app.get("/schema")
def get_schema():
    return {
        "animal": Animal.model_json_schema(),
        "sighting": Sighting.model_json_schema(),
        "volunteer": Volunteer.model_json_schema(),
        "donation": Donation.model_json_schema(),
    }

# Animals
@app.get("/api/animals")
def list_animals(limit: Optional[int] = 50):
    try:
        docs = get_documents("animal", {}, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/animals")
def create_animal(animal: Animal):
    try:
        inserted_id = create_document("animal", animal)
        return {"id": inserted_id, "message": "Animal added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sightings
@app.get("/api/sightings")
def list_sightings(limit: Optional[int] = 100):
    try:
        docs = get_documents("sighting", {}, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sightings")
def report_sighting(sighting: Sighting):
    try:
        inserted_id = create_document("sighting", sighting)
        return {"id": inserted_id, "message": "Sighting reported"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Volunteers
@app.post("/api/volunteers")
def sign_up_volunteer(volunteer: Volunteer):
    try:
        inserted_id = create_document("volunteer", volunteer)
        return {"id": inserted_id, "message": "Thanks for volunteering!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Donations (pledges)
@app.post("/api/donations")
def donation_pledge(donation: Donation):
    try:
        inserted_id = create_document("donation", donation)
        return {"id": inserted_id, "message": "Thank you for your pledge!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
