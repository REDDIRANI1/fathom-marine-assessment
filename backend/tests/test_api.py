import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def app():
    from app.main import app
    app.dependency_overrides[get_db] = override_get_db
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.fixture
def admin_headers(client):
    client.post("/api/v1/auth/register", json={
        "email": "admin@fathom.com",
        "password": "admin123",
        "name": "Admin User",
        "role": "admin",
    })
    resp = client.post("/api/v1/auth/login", json={
        "email": "admin@fathom.com",
        "password": "admin123",
    })
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}

@pytest.fixture
def crew_headers(client, admin_headers):
    client.post("/api/v1/ships", json={"name": "Test Ship"}, headers=admin_headers)
    ship_resp = client.get("/api/v1/ships", headers=admin_headers)
    ship_id = ship_resp.json()[0]["id"]

    client.post("/api/v1/auth/register", json={
        "email": "crew@fathom.com",
        "password": "crew123",
        "name": "Crew User",
        "role": "crew",
        "ship_id": ship_id,
    })
    resp = client.post("/api/v1/auth/login", json={
        "email": "crew@fathom.com",
        "password": "crew123",
    })
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}

def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Fathom Marine API"

def test_register_login(client):
    resp = client.post("/api/v1/auth/register", json={
        "email": "test@test.com",
        "password": "test123",
        "name": "Test",
        "role": "admin",
    })
    assert resp.status_code == 201
    assert "access_token" in resp.json()

    resp = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "test123",
    })
    assert resp.status_code == 200

def test_crew_registration_requires_ship(client):
    resp = client.post("/api/v1/auth/register", json={
        "email": "crew-no-ship@test.com",
        "password": "test123",
        "name": "Crew Without Ship",
        "role": "crew",
    })
    assert resp.status_code == 422
    assert resp.json()["detail"] == "Crew members must be assigned to a ship"

def test_registration_rejects_unknown_ship(client):
    resp = client.post("/api/v1/auth/register", json={
        "email": "crew-bad-ship@test.com",
        "password": "test123",
        "name": "Crew Bad Ship",
        "role": "crew",
        "ship_id": "00000000-0000-0000-0000-000000000000",
    })
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Selected ship was not found"

def test_create_ship(client, admin_headers):
    resp = client.post("/api/v1/ships", json={"name": "Ship Alpha"}, headers=admin_headers)
    assert resp.status_code == 201
    assert resp.json()["name"] == "Ship Alpha"

def test_crew_cannot_create_ship(client, crew_headers):
    resp = client.post("/api/v1/ships", json={"name": "Ship Beta"}, headers=crew_headers)
    assert resp.status_code == 403

def test_task_lifecycle(client, admin_headers):
    resp = client.post("/api/v1/ships", json={"name": "Task Ship"}, headers=admin_headers)
    ship_id = resp.json()["id"]

    resp = client.post("/api/v1/tasks", json={
        "title": "Engine check",
        "due_date": "2026-06-01",
        "ship_id": ship_id,
    }, headers=admin_headers)
    assert resp.status_code == 201
    task_id = resp.json()["id"]

    resp = client.patch(f"/api/v1/tasks/{task_id}/status", json={"status": "in_progress"}, headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "in_progress"

    resp = client.post(f"/api/v1/tasks/{task_id}/comments", json={"content": "Working on it"}, headers=admin_headers)
    assert resp.status_code == 201
    assert resp.json()["content"] == "Working on it"

    resp = client.patch(f"/api/v1/tasks/{task_id}/status", json={"status": "completed"}, headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"

def test_drill_lifecycle(client, admin_headers):
    resp = client.post("/api/v1/ships", json={"name": "Drill Ship"}, headers=admin_headers)
    ship_id = resp.json()["id"]

    resp = client.post("/api/v1/drills", json={
        "drill_type": "fire",
        "scheduled_date": "2026-06-15",
        "ship_id": ship_id,
    }, headers=admin_headers)
    assert resp.status_code == 201
    drill_id = resp.json()["id"]

    resp = client.patch(f"/api/v1/drills/{drill_id}/complete", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"

def test_compliance_calculation(client, admin_headers):
    resp = client.post("/api/v1/ships", json={"name": "Compliance Ship"}, headers=admin_headers)
    ship_id = resp.json()["id"]

    client.post("/api/v1/tasks", json={
        "title": "Task 1",
        "due_date": "2026-06-01",
        "ship_id": ship_id,
    }, headers=admin_headers)

    client.post("/api/v1/drills", json={
        "drill_type": "fire",
        "scheduled_date": "2026-06-15",
        "ship_id": ship_id,
    }, headers=admin_headers)

    resp = client.get("/api/v1/compliance", headers=admin_headers)
    assert resp.status_code == 200
    stats = resp.json()
    assert stats["maintenance_pct"] == 0.0
    assert stats["drill_pct"] == 0.0
    assert stats["overdue_tasks"] == 0
    assert stats["missed_drills"] == 0
