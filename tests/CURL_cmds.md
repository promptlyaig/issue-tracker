
## ⚙️ Server info

Make sure your server is running:

```bash
uvicorn app.01_issue_tracker:app --reload --host 0.0.0.0 --port 8888
```

Base URL:

```bash
BASE_URL=http://localhost:8888
```

---

## 🩺 1. Health Check Endpoints

### ✅ Root Endpoint

```bash
curl -X GET "$BASE_URL/"
# Expected: {"status": "I am Root"}
```

### ✅ Health Endpoint

```bash
curl -X GET "$BASE_URL/health"
# Expected: {"status": "ok"}
```

---

## 🧾 2. Create Issue

### ✅ Valid request

```bash
curl -X POST "$BASE_URL/issues" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=Printer not working" \
  -d "deportment_id=111" \
  -d "assignee_name=saketh"

# Expected: 201 Created
# {
#   "id": "auto-generated-uuid",
#   "title": "Printer not working",
#   "deportment_id": "111",
#   "assignee_name": "saketh",
#   "is_deleted": false
# }
```

### ❌ Invalid deportment ID

```bash
curl -X POST "$BASE_URL/issues" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=Invalid test" \
  -d "deportment_id=999" \
  -d "assignee_name=tester"

# Expected: 400 Bad Request
# {"detail":{"error":"invalid_request","message":"deportment_id is invalid"}}
```

---

## 📋 3. List All Issues

```bash
curl -X GET "$BASE_URL/issues"

# Expected: 200 OK
# [
#   {
#     "id": "uuid",
#     "title": "Printer not working",
#     "deportment_id": "111",
#     "assignee_name": "saketh",
#     "is_deleted": false
#   }
# ]
```

---

## 🔍 4. Get Issue by ID

(Replace `<ISSUE_ID>` with actual UUID returned from create)

```bash
curl -X GET "$BASE_URL/issues/<ISSUE_ID>"

# Expected: 200 OK
# {
#   "id": "<ISSUE_ID>",
#   "title": "Printer not working",
#   "deportment_id": "111",
#   "assignee_name": "saketh",
#   "is_deleted": false
# }
```

If the ID doesn’t exist:

```bash
curl -X GET "$BASE_URL/issues/nonexistent-id"
# Expected: 404 Not Found
```

---

## ✏️ 5. Update Issue

(Replace `<ISSUE_ID>` with actual UUID)

```bash
curl -X PUT "$BASE_URL/issues/<ISSUE_ID>" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=Printer repaired" \
  -d "assignee_name=bhagavan"

# Expected: 200 OK
# Updated issue object with modified fields
```

❌ Example of invalid department ID:

```bash
curl -X PUT "$BASE_URL/issues/<ISSUE_ID>" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "deportment_id=999"
# Expected: 400 Bad Request
```

---

## 🗑️ 6. Delete Issue (Soft Delete)

```bash
curl -X DELETE "$BASE_URL/issues/<ISSUE_ID>"
# Expected: 204 No Content
```

Then, if you list again:

```bash
curl -X GET "$BASE_URL/issues"
# The deleted issue should no longer appear in the list
```

---

## 🏢 7. List All Deportments

```bash
curl -X GET "$BASE_URL/deportments"

# Expected: 200 OK
# [
#   {"id": "111", "name": "HR", "description": "Human Resources"},
#   {"id": "222", "name": "Finance", "description": "Finance & Accounts"},
#   {"id": "333", "name": "IT", "description": "Information Technology"}
# ]
```

---

## 🧠 Summary of all endpoints

| HTTP Method | Endpoint       | Description                |
| ----------- | -------------- | -------------------------- |
| GET         | `/`            | Root health check          |
| GET         | `/health`      | Basic service health check |
| POST        | `/issues`      | Create a new issue         |
| GET         | `/issues`      | List all issues            |
| GET         | `/issues/{id}` | Retrieve single issue      |
| PUT         | `/issues/{id}` | Update issue details       |
| DELETE      | `/issues/{id}` | Soft delete an issue       |
| GET         | `/deportments` | List static departments    |

