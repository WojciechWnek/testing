def test_get_wrestlers(client):
    response = client.get("/wrestlers")
    assert response.status_code == 200
    assert response.json() == []
