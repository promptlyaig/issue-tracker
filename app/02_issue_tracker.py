from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from uuid import uuid4

class Issue(BaseModel):
    id: str
    title: str
    deportment_id: str
    assignee_name: Optional[str] = None
    is_deleted: bool = False

app = FastAPI(title="Issue Tracker", version="0.3")

# --- Static deportments (hard-coded, read-only) ---
STATIC_DEPORTMENTS: Dict[str, Dict[str, str]] = {
    "111": {"id": "111", "name": "HR", "description": "Human Resources"},
    "222": {"id": "222", "name": "Finance", "description": "Finance & Accounts"},
    "333": {"id": "333", "name": "IT", "description": "Information Technology"},
}

# --- In-memory issues store ---
issues: Dict[str, Issue] = {}

@app.get("/")
async def root_health():
    return {"status": "I am Root"}

@app.get("/health")
async def health():
    """Health endpoint for the Issue Tracker service."""
    return {"status": "ok"}

# --- Create issue (simplified form input) ---
@app.post("/issues", response_model=Issue, status_code=201)
async def create_issue(
    title: str = Form(..., description="Issue title"),
    deportment_id: str = Form(..., description="ID of the static deportment"),
    assignee_name: Optional[str] = Form(None, description="Name of the assignee"),
):
    """Create a new issue (form input, minimal fields)."""
    deportment_id_str = str(deportment_id)
    if deportment_id_str not in STATIC_DEPORTMENTS:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_request", "message": "deportment_id is invalid"},
        )

    new_id = str(uuid4())  # store id as string
    issue = Issue(
        id=new_id,
        title=title,
        deportment_id=deportment_id,
        assignee_name=assignee_name,
    )
    issues[new_id] = issue
    return issue
