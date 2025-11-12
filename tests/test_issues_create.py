# tests/test_issues_create_client.py
import requests

BASE_URL = "http://localhost:8888"

def test_create_issue_success():
    """Test: successfully create an issue."""
    url = f"{BASE_URL}/issues"
    data = {
        "title": "test1",
        "deportment_id": "111",
        "assignee_name": "saketh",
    }

    response = requests.post(url, data=data)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    issue = response.json()

    assert issue["title"] == data["title"]
    assert issue["deportment_id"] == data["deportment_id"]
    assert issue["assignee_name"] == data["assignee_name"]
    assert "id" in issue
    print("✅ test_create_issue_success passed")


def test_create_issue_invalid_deportment():
    """Test: creation fails with invalid deportment ID."""
    url = f"{BASE_URL}/issues"
    data = {
        "title": "invalid",
        "deportment_id": "999",  # invalid ID
        "assignee_name": "anyone",
    }

    response = requests.post(url, data=data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("✅ test_create_issue_invalid_deportment passed")


if __name__ == "__main__":
    print("🚀 Running create issue endpoint tests...")
    test_create_issue_success()
    test_create_issue_invalid_deportment()
    print("🎉 All create-issue tests passed successfully!")
