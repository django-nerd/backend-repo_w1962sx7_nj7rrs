import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Lead, Project, Testimonial, Service

app = FastAPI(title="Agency CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Agency CRM Backend Running"}

# Health check including DB
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
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

# Public endpoints to power the website

@app.get("/api/projects", response_model=List[Project])
def list_projects(limit: int = 12):
    docs = get_documents("project", {}, limit)
    # Convert Mongo docs to pydantic-compatible dicts
    for d in docs:
        d.pop("_id", None)
    return docs

@app.get("/api/testimonials", response_model=List[Testimonial])
def list_testimonials(limit: int = 12):
    docs = get_documents("testimonial", {}, limit)
    for d in docs:
        d.pop("_id", None)
    return docs

@app.get("/api/services", response_model=List[Service])
def list_services(limit: int = 12):
    docs = get_documents("service", {}, limit)
    for d in docs:
        d.pop("_id", None)
    return docs

class LeadResponse(BaseModel):
    success: bool
    message: str

@app.post("/api/leads", response_model=LeadResponse)
def create_lead(lead: Lead):
    try:
        create_document("lead", lead)
        return {"success": True, "message": "Thanks! We'll get back to you within 24 hours."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional seed endpoint to populate demo data if collections are empty
@app.post("/api/seed")
def seed_data():
    try:
        if db is None:
            raise Exception("Database not configured")
        # Only seed if empty
        if db["project"].count_documents({}) == 0:
            create_document("project", {"title": "SaaS Analytics Dashboard", "description": "Real-time metrics, role-based access, and stunning UI.", "tags": ["React", "Tailwind", "FastAPI"], "url": "https://example.com", "image": "/projects/saas.png", "highlight": True})
            create_document("project", {"title": "E-commerce Storefront", "description": "High-converting storefront with checkout and CMS.", "tags": ["Next.js", "Stripe", "Sanity"], "image": "/projects/store.png"})
        if db["testimonial"].count_documents({}) == 0:
            create_document("testimonial", {"name": "Ava Patel", "role": "COO, Nimbus Labs", "quote": "They delivered ahead of schedule with exceptional quality.", "avatar": "/avatars/ava.png"})
            create_document("testimonial", {"name": "Marcus Lee", "role": "Founder, Drift.io", "quote": "Our conversion rate jumped 37% after launch.", "avatar": "/avatars/marcus.png"})
        if db["service"].count_documents({}) == 0:
            create_document("service", {"name": "Product Strategy", "description": "From idea to roadmap with business outcomes.", "icon": "Lightbulb"})
            create_document("service", {"name": "Design & Frontend", "description": "Beautiful, accessible UI with motion.", "icon": "Palette"})
            create_document("service", {"name": "Web Apps & APIs", "description": "Robust backends with integrations.", "icon": "Server"})
        return {"seeded": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
