import pytest


def test_get_wrestlers(client):
    response = client.get("/wrestlers")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.usefixtures("wrestler")
def test_get_wrestlers_after_create(client):
    response = client.get("/wrestlers")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.usefixtures("wrestler")
def test_search_wrestlers_by_name(client, inactive_wrestler):
    response = client.get("/wrestlers/search", params={"name": "rock"})
    assert response.status_code == 200

    wrestlers = response.json()
    assert [wrestler["id"] for wrestler in wrestlers] == [inactive_wrestler.id]


@pytest.mark.usefixtures("inactive_wrestler")
def test_search_wrestlers_by_active(client, wrestler):
    response = client.get("/wrestlers/search", params={"active": True})
    assert response.status_code == 200

    wrestlers = response.json()
    assert [wrestler["id"] for wrestler in wrestlers] == [wrestler.id]


@pytest.mark.usefixtures("wrestler")
def test_search_wrestlers_no_results(client):
    response = client.get("/wrestlers/search", params={"name": "silly"})
    assert response.status_code == 200
    assert response.json() == []


def test_search_wrestlers_without_params_returns_all_wrestlers(
    client, wrestler, inactive_wrestler
):
    response = client.get("/wrestlers/search")
    assert response.status_code == 200

    wrestlers = response.json()
    assert [wrestler["id"] for wrestler in wrestlers] == [
        wrestler.id,
        inactive_wrestler.id,
    ]


def test_get_wrestler_by_id(client, wrestler):
    get_response = client.get(f"/wrestlers/{wrestler.id}")
    assert get_response.status_code == 200

    fetched_wrestler = get_response.json()
    assert fetched_wrestler["id"] == wrestler.id
    assert fetched_wrestler["name"] == wrestler.name


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


def test_update_wrestler(client, wrestler):
    patch_response = client.patch(
        f"/wrestlers/{wrestler.id}", json={"finisher": "Chokeslam"}
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["finisher"] == "Chokeslam"


def test_update_nonexistent_wrestler_returns_not_found(client):
    response = client.patch("/wrestlers/999", json={"finisher": "Chokeslam"})
    assert response.status_code == 404


def test_delete_wrestler(client, wrestler):
    response = client.delete(f"/wrestlers/{wrestler.id}")
    assert response.status_code == 204

    response = client.delete(f"/wrestlers/{wrestler.id}")
    assert response.status_code == 404

    response = client.get(f"/wrestlers/{wrestler.id}")
    assert response.status_code == 404
