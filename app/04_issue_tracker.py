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

# --- List all issues (non-deleted) ---
@app.get("/issues", response_model=List[Issue])
async def list_issues():
    """Return all non-deleted issues."""
    return [i for i in issues.values() if not i.is_deleted]

@app.get("/issues/{issue_id}", response_model=Issue)
async def get_issue(issue_id: str):
    """Retrieve an issue by its ID."""
    if issue_id not in issues or issues[issue_id].is_deleted:
        raise HTTPException(status_code=404, detail={"error": "not_found", "message": "issue not found"})
    
    return issues[issue_id]

# --- Expose static deportments (read-only) ---
@app.get("/deportments")
async def list_deportments():
    """Return the predefined static deportments."""
    return list(STATIC_DEPORTMENTS.values())

@app.get("/deportments/{deportment_id}")
async def get_deportment(deportment_id: str):
    if deportment_id not in STATIC_DEPORTMENTS:
        raise HTTPException(status_code=404, detail={"error": "not_found", "message": "deportment not found"})
    return STATIC_DEPORTMENTS[deportment_id]

