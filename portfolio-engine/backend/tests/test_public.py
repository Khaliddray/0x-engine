def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "version" in data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_public_portfolio_not_found(client):
    response = client.get("/api/public/portfolios/nonexistent-portfolio")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_public_portfolio_success_unauthenticated(client, auth_headers):
    # Setup portfolio and child entities using authenticated client
    p_res = client.post(
        "/api/portfolios",
        json={
            "name": "Khalid Yahaya",
            "slug": "khalid",
            "description": "Full-stack engineer & architect",
        },
        headers=auth_headers,
    )
    assert p_res.status_code == 201
    p_id = p_res.json()["id"]

    # Add project
    prj_res = client.post(
        "/api/projects",
        json={
            "portfolio_id": p_id,
            "title": "Portfolio Engine",
            "slug": "portfolio-engine",
            "description": "FastAPI content engine",
            "is_featured": True,
        },
        headers=auth_headers,
    )
    assert prj_res.status_code == 201
    prj_id = prj_res.json()["id"]

    # Add technology to project
    tech_res = client.post(
        "/api/project-technologies",
        json={"project_id": prj_id, "name": "Python", "slug": "python", "position": 1},
        headers=auth_headers,
    )
    assert tech_res.status_code == 201

    # Add skill to portfolio
    skill_res = client.post(
        "/api/skills",
        json={"portfolio_id": p_id, "name": "FastAPI", "slug": "fastapi", "position": 1},
        headers=auth_headers,
    )
    assert skill_res.status_code == 201

    # Public request without authentication header
    pub_res = client.get("/api/public/portfolios/khalid")
    assert pub_res.status_code == 200
    data = pub_res.json()

    assert data["name"] == "Khalid Yahaya"
    assert data["slug"] == "khalid"
    assert len(data["projects"]) == 1
    assert data["projects"][0]["title"] == "Portfolio Engine"
    assert data["projects"][0]["is_featured"] is True
    assert len(data["projects"][0]["technologies"]) == 1
    assert data["projects"][0]["technologies"][0]["name"] == "Python"
    assert len(data["skills"]) == 1
    assert data["skills"][0]["name"] == "FastAPI"
