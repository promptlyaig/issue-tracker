# tests/test_health_client.py
import requests

BASE_URL = "http://localhost:8888"

def test_root_health():
    """Test the root ('/') health endpoint."""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert response.json() == {"status": "I am Root"}
    print("✅ / endpoint test passed")

def test_health():
    """Test the '/health' endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert response.json() == {"status": "ok"}
    print("✅ /health endpoint test passed")


if __name__ == "__main__":
    test_root_health()
    test_health()
    print("🎉 All health tests passed successfully!")
