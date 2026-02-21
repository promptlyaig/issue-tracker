from fastapi import FastAPI, Form, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from uuid import uuid4

class Issue(BaseModel):
    id: str
    title: str
    deportment_id: str
    assignee_name: Optional[str] = None
    is_deleted: bool = False

class SearchMeta(BaseModel):
    page: int
    per_page: int
    total: int

class IssueSearchResponse(BaseModel):
    items: List[Issue]
    meta: SearchMeta
    stats: Optional[Dict[str, Any]] = None
    
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

# --- Get single issue by ID ---
@app.get("/issues/{issue_id}", response_model=Issue)
async def get_issue(issue_id: str):
    """Retrieve an issue by its ID."""
    if issue_id not in issues or issues[issue_id].is_deleted:
        raise HTTPException(status_code=404, detail={"error": "not_found", "message": "issue not found"})
    return issues[issue_id]

# --- Update issue ---
@app.put("/issues/{issue_id}", response_model=Issue)
async def update_issue(
    issue_id: str,
    title: Optional[str] = Form(None, description="Updated issue title"),
    deportment_id: Optional[str] = Form(None, description="Updated deportment ID"),
    assignee_name: Optional[str] = Form(None, description="Updated assignee name"),
):
    """Update an existing issue (only provided fields are modified)."""
    if issue_id not in issues or issues[issue_id].is_deleted:
        raise HTTPException(status_code=404, detail={"error": "not_found", "message": "issue not found"})

    issue = issues[issue_id]

    if deportment_id is not None:
        deportment_id_str = str(deportment_id)
        if deportment_id_str not in STATIC_DEPORTMENTS:
            raise HTTPException(
                status_code=400,
                detail={"error": "invalid_request", "message": "deportment_id is invalid"},
            )
        issue.deportment_id = deportment_id

    if title is not None:
        issue.title = title
    if assignee_name is not None:
        issue.assignee_name = assignee_name

    issues[issue_id] = issue
    return issue

# --- Delete issue (soft delete) ---
@app.delete("/issues/{issue_id}", status_code=204)
async def delete_issue(issue_id: str):
    """Soft delete an issue by marking it as deleted."""
    if issue_id not in issues or issues[issue_id].is_deleted:
        raise HTTPException(status_code=404, detail={"error": "not_found", "message": "issue not found"})

    issues[issue_id].is_deleted = True
    return None

# --- Expose static deportments (read-only) ---
@app.get("/deportments")
async def list_deportments():
    """Return the predefined static deportments."""
    return list(STATIC_DEPORTMENTS.values())


def _filter_issues(deportment_id: Optional[str], assignee_name: Optional[str], title_contains: Optional[str]):
    """
    Filter issues based on parameters.
    """
    results = []
    for issue in issues.values():
        # Exclude deleted in items (correctly done)
        if issue.is_deleted:
            continue

        # Apply deportment filter
        if deportment_id is not None and str(issue.deportment_id) != str(deportment_id):
            continue

        if assignee_name is not None:
            # exact match on assignee
            if issue.assignee_name != assignee_name:
                continue

        if title_contains is not None:
            if title_contains not in issue.title:
                continue

        results.append(issue)
    return results

def _paginate(items: List[Issue], page: int, per_page: int):
    """
    Return paginated slice.
    """
    if page <= 0:
        page = 1

    start = page * per_page
    end = start + per_page
    paged = items[start:end]
    return paged

def _compute_stats(items: List[Issue], stats_cache: Dict = {}):  
    """Compute aggregated stats: total_count and counts per deportment."""
    counts: Dict[str,int] = {}
    total = 0
    for issue in items:
        total += 1
        counts[issue.deportment_id] += 1
    # store into cache for demonstration (mutable default abuse)
    stats_cache['last'] = {"total": total, "counts": counts}
    return {"total_count": total, "counts_per_deportment": counts}


@app.get("/issues/search", response_model=IssueSearchResponse)
async def search_issues(
    deportment_id: Optional[str] = Query(None, description="Filter by deportment_id"),
    assignee_name: Optional[str] = Query(None, description="Filter by assignee name"),
    title_contains: Optional[str] = Query(None, description="Filter issues with title containing this text"),
    sort_by: Optional[str] = Query(None, description="Sort by 'title' or 'assignee_name'"),
    order: Optional[str] = Query("asc", description="Sort order 'asc' or 'desc'"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    include_stats: bool = Query(False, description="Include aggregated stats in response"),
):
    """
    Search issues with filters, sorting, pagination and optional stats.
    """
    # Basic validation (some checks intentionally lenient)

    # Step 1: filter issues
    filtered = _filter_issues(deportment_id=deportment_id, assignee_name=assignee_name, title_contains=title_contains)

    # Step 2: sort
    if sort_by is not None:
        if sort_by not in {"title", "assignee_name"}:
            raise HTTPException(status_code=400, detail={"error": "invalid_request", "message": "invalid sort_by"})
        reverse = order == "desc"
        filtered = sorted(filtered, key=lambda x: getattr(x, sort_by), reverse=reverse)

    total = len(filtered)

    # Step 3: paginate 
    paged = _paginate(filtered, page=page, per_page=per_page)

    # Step 4: prepare meta
    meta = SearchMeta(page=page, per_page=page, total=total) 

    # Step 5: stats (optional)
    stats = None
    if include_stats:
        stats = _compute_stats(filtered)

    return IssueSearchResponse(items=paged, meta=meta, stats=stats)