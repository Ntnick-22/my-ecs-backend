def register(client, name="Ada", email="ada@example.com", role="Engineer"):
    return client.post("/api/register", json={"name": name, "email": email, "role": role})


def test_health_reports_database_connected(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["database"] == "connected"


def test_ready(client):
    assert client.get("/api/ready").status_code == 200


def test_register_creates_user(client):
    r = register(client)
    assert r.status_code == 201
    user = r.get_json()["user"]
    assert user["email"] == "ada@example.com"
    assert user["role"] == "Engineer"


def test_register_normalises_email(client):
    r = register(client, email="  ADA@Example.COM ")
    assert r.get_json()["user"]["email"] == "ada@example.com"


def test_register_requires_name_and_email(client):
    r = client.post("/api/register", json={"name": "Ada"})
    assert r.status_code == 400


def test_register_duplicate_email_is_409(client):
    register(client)
    r = register(client, name="Someone else")
    assert r.status_code == 409


def test_list_users(client):
    register(client)
    register(client, name="Bob", email="bob@example.com")
    users = client.get("/api/users").get_json()["users"]
    assert {u["email"] for u in users} == {"ada@example.com", "bob@example.com"}


def test_stats(client):
    # Drill E (2026-10-07) broke this endpoint with a column typo; only a real database catches that
    register(client, role="Engineer")
    register(client, name="Bob", email="bob@example.com", role="Student")
    register(client, name="Cy", email="cy@example.com", role="Student")
    r = client.get("/api/stats")
    assert r.status_code == 200
    assert r.get_json() == {"total_users": 3, "today_users": 3, "total_roles": 2}


def test_delete_user(client):
    user_id = register(client).get_json()["user"]["id"]
    assert client.delete(f"/api/users/{user_id}").status_code == 200
    assert client.delete(f"/api/users/{user_id}").status_code == 404
