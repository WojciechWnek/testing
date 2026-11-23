def test_set_theme_cookie(client):
    response = client.post("/theme", json={"value": "dark"})

    assert response.status_code == 201
    assert response.cookies["theme"] == "dark"


def test_set_invalid_theme(client):
    response = client.post("/theme", json={"value": "purple"})
    assert response.status_code == 422


def test_get_theme_with_cookie(client):
    client.cookies.set("theme", "dark")

    response = client.get("/theme")
    assert response.status_code == 200
    assert response.json() == {"theme": "dark"}
