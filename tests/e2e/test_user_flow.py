def test_login_quote(client):
    res = client.post("/login", data={})
    assert res.status_code in (302, 200)

    res = client.get("/quote")
    assert res.status_code == 200
