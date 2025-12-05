def test_create_and_read_calc(db_session, client):
    r = client.post("/calculations", json={"a": 5, "b": 3, "type": "add"})
    assert r.status_code == 200

    data = r.json()
    assert data["result"] == 8
    assert "id" in data

    calc_id = data["id"]


    r2 = client.get(f"/calculations/{calc_id}")
    assert r2.status_code == 200
    assert r2.json()["result"] == 8
