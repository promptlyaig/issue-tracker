# 🧾 Issue Tracker API

A simple, lightweight **FastAPI-based REST server** for managing internal issues raised by different departments like HR, Finance, and IT. This version supports full CRUD operations on issues, using in-memory storage (no database) and static department definitions.

---

## 🚀 Version 1 — Health Check Only
- `/` → Root health endpoint (returns `{"status": "I am Root"}`)
- `/health` → Basic health check endpoint (returns `{"status": "ok"}`)

---

## 🧩 Version 2 — Issues CRUD Endpoints

### Create Issue
**POST** `/issues`
- Form input fields:
  - `title` *(required)* — Issue title
  - `deportment_id` *(required)* — Department ID (one of `111`, `222`, or `333`)
  - `assignee_name` *(optional)* — Name of the assignee

**Example (cURL):**
```bash
curl -X POST "http://localhost:8888/issues" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=PrinterDown" \
  -d "deportment_id=111" \
  -d "assignee_name=saketh"
```

### List Issues
**GET** `/issues`
- Returns a list of all active (non-deleted) issues.

### Get Single Issue
**GET** `/issues/{issue_id}`
- Retrieves a specific issue by its ID.

### Update Issue
**PUT** `/issues/{issue_id}`
- Form input fields (all optional):
  - `title` — Updated title
  - `deportment_id` — Updated department ID
  - `assignee_name` — Updated assignee name

### Delete Issue (Soft Delete)
**DELETE** `/issues/{issue_id}`
- Marks the issue as deleted (`is_deleted = True`), it won’t appear in list results.

### List Departments
**GET** `/deportments`
- Returns a static list of available departments.

---

## 🧠 Notes
- All data is stored **in-memory** and resets when the server restarts.
- No authentication or concurrency mechanisms.
- Department IDs are fixed (`111`, `222`, `333`).

---

## ▶️ How to Run
```sh
cd issue_tracker
uvicorn app.01_issue_tracker:app --reload --host 0.0.0.0 --port 8888
```

---

## 🌐 How to Browse
```url
http://localhost:8888/docs
```
Use the Swagger UI to test each endpoint interactively.