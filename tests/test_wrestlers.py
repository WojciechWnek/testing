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


def test_search_wrestlers_by_name(client):
    client.post(
        "/wrestlers",
        json={
            "name": "The Undertaker",
            "finisher": "Tombstone Piledriver",
            "catchphrase": "Rest in peace",
        },
    )

    rock = client.post(
        "/wrestlers",
        json={
            "name": "The Rock",
            "finisher": "Rock Bottom",
            "catchphrase": "Can you smell what the Rock is cooking?",
        },
    )

    response = client.get("/wrestlers/search", params={"name": "rock"})
    assert response.status_code == 200

    wrestlers = response.json()
    assert [wrestler["id"] for wrestler in wrestlers] == [rock.json()["id"]]


def test_search_wrestlers_by_active(client):
    undertaker = client.post(
        "/wrestlers",
        json={
            "name": "The Undertaker",
            "finisher": "Tombstone Piledriver",
            "catchphrase": "Rest in peace",
            "active": True,
        },
    )

    client.post(
        "/wrestlers",
        json={
            "name": "The Rock",
            "finisher": "Rock Bottom",
            "catchphrase": "Can you smell what the Rock is cooking?",
            "active": False,
        },
    )

    response = client.get("/wrestlers/search", params={"active": True})
    assert response.status_code == 200

    wrestlers = response.json()
    assert [wrestler["id"] for wrestler in wrestlers] == [undertaker.json()["id"]]


def test_search_wrestlers_no_results(client):
    client.post(
        "/wrestlers",
        json={
            "name": "The Undertaker",
            "finisher": "Tombstone Piledriver",
            "catchphrase": "Rest in peace",
        },
    )

    response = client.get("/wrestlers/search", params={"name": "silly"})
    assert response.status_code == 200
    assert response.json() == []


def test_search_wrestlers_without_params_returns_all_wrestlers(client):
    undertaker = client.post(
        "/wrestlers",
        json={
            "name": "The Undertaker",
            "finisher": "Tombstone Piledriver",
            "catchphrase": "Rest in peace",
            "active": True,
        },
    )

    rock = client.post(
        "/wrestlers",
        json={
            "name": "The Rock",
            "finisher": "Rock Bottom",
            "catchphrase": "Can you smell what the Rock is cooking?",
            "active": False,
        },
    )

    response = client.get("/wrestlers/search")
    assert response.status_code == 200

    wrestlers = response.json()
    assert [wrestler["id"] for wrestler in wrestlers] == [
        undertaker.json()["id"],
        rock.json()["id"],
    ]


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


def test_update_wrestler(client):
    create_response = client.post(
        "/wrestlers",
        json={
            "name": "The Undertaker",
            "finisher": "Tombstone Piledriver",
            "catchphrase": "Rest in peace",
        },
    )

    assert create_response.status_code == 201

    undertaker = create_response.json()
    wrestler_id = undertaker["id"]

    patch_response = client.patch(
        f"/wrestlers/{wrestler_id}", json={"finisher": "Chokeslam"}
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["finisher"] == "Chokeslam"


def test_update_nonexistent_wrestler_returns_not_found(client):
    response = client.patch("/wrestlers/999", json={"finisher": "Chokeslam"})
    assert response.status_code == 404


def test_delete_wrestler(client):
    create_response = client.post(
        "/wrestlers",
        json={
            "name": "The Undertaker",
            "finisher": "Tombstone Piledriver",
            "catchphrase": "Rest in peace",
        },
    )

    assert create_response.status_code == 201

    undertaker = create_response.json()
    wrestler_id = undertaker["id"]

    response = client.delete(f"/wrestlers/{wrestler_id}")
    assert response.status_code == 204

    response = client.delete(f"/wrestlers/{wrestler_id}")
    assert response.status_code == 404

    response = client.get(f"/wrestlers/{wrestler_id}")
    assert response.status_code == 404
