import os
import pytest

# Ensure SQLite memory database is used for testing
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-32-chars-minimum-length"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # Registers all models on Base.metadata
from app.core.security import hash_password
from app.db.session import Base, get_db
from app.main import app
from app.models.user import User


engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    """Provide a transactional database session for a test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    """Provide a FastAPI TestClient with overridden database session."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """Create and return an active standard test user."""
    user = User(
        email="developer@example.com",
        hashed_password=hash_password("DevPassword123!"),
        full_name="Yahaya Khalid",
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Log in the standard user and return Bearer token headers."""
    response = client.post(
        "/api/auth/login",
        json={"email": "developer@example.com", "password": "DevPassword123!"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def superuser(db):
    """Create and return an active superuser."""
    user = User(
        email="admin@example.com",
        hashed_password=hash_password("AdminPassword123!"),
        full_name="Super Admin",
        is_active=True,
        is_superuser=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def superuser_headers(client, superuser):
    """Log in the superuser and return Bearer token headers."""
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "AdminPassword123!"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
