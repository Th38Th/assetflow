from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Necessary setup fixtures
@pytest.fixture(scope="session")
def client(request):
    base_url = request.config.getoption("--base-url")
    # You can create a TestClient or a real HTTP client depending on base_url
    # For local TestClient (no actual HTTP requests):
    if base_url is None:
        return TestClient(app)
    else:
        # For real HTTP requests to a running server, you might want to use requests directly:
        import requests
        class RequestsClient:
            def get(self, path, **kwargs):
                return requests.get(base_url + path, **kwargs)
            def post(self, path, **kwargs):
                return requests.post(base_url + path, **kwargs)
            def delete(self, path, **kwargs):
                return requests.delete(base_url + path, **kwargs)
            def put(self, path, **kwargs):
                return requests.put(base_url + path, **kwargs)
            def patch(self, path, **kwargs):
                return requests.patch(base_url + path, **kwargs)
        return RequestsClient()

@pytest.fixture(scope="session")
def test_user(client):
    user_name = f"testuser{datetime.now(timezone.utc).strftime('%Y-%m-%d.%H:%M:%S')}"
    user_password = f"{user_name}p@$&"
    client.post("/auth/signup", json={"username": user_name, "password": user_password})
    return {"username": user_name, "password": user_password}

@pytest.fixture(scope="session")
def auth_token(client,test_user):
    response = client.post("/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    return response.json()["access_token"]

@pytest.fixture
def item_ids(client,auth_token):
    response = client.get("/assets", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    return [x["id"] for x in response.json()]

# Begin actual tests

def test_read_root(client):
    """Sanity check to see if the root path returns the expected message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_existing_username(client, test_user):
    """Test if username uniqueness is enforced"""
    response = client.post("/auth/signup", json={"username": test_user["username"], "password": "newPass"})
    assert response.status_code == 400

def test_get_items_empty(client, auth_token):
    """Test if an empty item list is returned (newly-created user)"""
    response = client.get("/assets", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert response.json() == []

def test_create_item(client, auth_token):
    """Test if an item is being created and return properly (with just name)"""
    response = client.post("/assets", json={"name": "test123"}, headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 201
    json = response.json()
    json.pop("id")
    assert json == {"name": "test123", "tags": None, "file_name": None}

def test_create_item_with_tags(client, auth_token):
    """Test if an item is being created and return properly (with name and tags)"""
    response = client.post("/assets", json={"name": "test456", "tags": ["new", "exciting", "real"]}, headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 201
    json = response.json()
    json.pop("id")
    assert json == {"name": "test456", "tags": ["new", "exciting", "real"], "file_name": None}

def test_get_item(client, item_ids, auth_token):
    """Test if requesting item by id returns correct item"""
    item_id = item_ids[0]
    response = client.get(f"/assets/{item_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert response.json() == {"id": item_id, "name": "test123", "tags": None, "file_name": None}

def test_get_item_with_tags(client, item_ids, auth_token):
    """Test if requesting item by id returns correct item (this item has tags too)"""
    item_id = item_ids[1]
    response = client.get(f"/assets/{item_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert response.json() == {"id": item_id, "name": "test456", "tags": ["new", "exciting", "real"], "file_name": None}

def test_delete_item(client, item_ids, auth_token):
    """Test if an item identified by id is properly deleted"""
    item_id = item_ids[0]
    response = client.delete(f"/assets/{item_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Item {item_id} deleted"
    }

def test_get_item_missing(client, auth_token):
    """Test if requesting invalid item by id returns correct message"""
    item_id = -1
    response = client.get(f"/assets/{item_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Asset not found or not accessible"
    }