def test_get_wrestlers(client):
    response = client.get("/wrestlers")
    assert response.status_code == 200
    assert response.json() == []


def test_get_wrestlers_after_create(client):
    response = client.post(
        "/wrestlers",
        json={
            "name": "The Undertaker",
            "finisher": "Tombstone Piledriver",
            "catchphrase": "Rest in peace",
            "active": True,
        },
    )

    assert response.status_code == 201

    response = client.get("/wrestlers")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_wrestler_by_id(client):
    create_response = client.post(
        "/wrestlers",
        json={
            "name": "The Undertaker",
            "finisher": "Tombstone Piledriver",
            "catchphrase": "Rest in peace",
            "active": True,
        },
    )

    assert create_response.status_code == 201

    created_wrestler = create_response.json()
    wrestler_id = created_wrestler["id"]

    get_response = client.get(f"/wrestlers/{wrestler_id}")
    assert get_response.status_code == 200

    fetched_wrestler = get_response.json()
    assert fetched_wrestler["id"] == created_wrestler["id"]
    assert fetched_wrestler["name"] == created_wrestler["name"]


def test_get_wrestler_not_found(client):
    response = client.get("/wrestlers/999")
    assert response.status_code == 404


def test_create_wrestler(client):
    response = client.post(
        "/wrestlers",
        json={
            "name": "The Undertaker",
            "finisher": "Tombstone Piledriver",
            "catchphrase": "Rest in peace",
            "active": True,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["name"] == "The Undertaker"


def test_create_wrestler_makes_active_by_default(client):
    response = client.post(
        "/wrestlers",
        json={
            "name": "The Undertaker",
            "finisher": "Tombstone Piledriver",
            "catchphrase": "Rest in peace",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["active"] is True
