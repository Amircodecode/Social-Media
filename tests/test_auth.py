async def test_register_user_success(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "strongpassword123",
            "full_name": "amir yusupov",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["is_verified"] is False


async def test_register_duplicate_email(client):
    payload = {
        "email": "dup@example.com",
        "password": "strongpassword123",
        "full_name": "amir yusupov",
    }
    await client.post("/auth/register", json=payload)
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 409


async def test_login_success(client):
    await client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "strongpassword123",
            "full_name": "amir yusupov",
        },
    )
    response = await client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "strongpassword123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_wrong_password(client):
    await client.post(
        "/auth/register",
        json={
            "email": "wrongpass@example.com",
            "password": "strongpassword123",
            "full_name": "amir yusupov",
        },
    )
    response = await client.post(
        "/auth/login",
        data={"username": "wrongpass@example.com", "password": "incorrect"},
    )
    assert response.status_code == 401


async def test_me_without_token(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401


async def test_me_with_token(client):
    await client.post(
        "/auth/register",
        json={
            "email": "me@example.com",
            "password": "strongpassword123",
            "full_name": "amir yusupov",
        },
    )
    login_response = await client.post(
        "/auth/login",
        data={"username": "me@example.com", "password": "strongpassword123"},
    )
    token = login_response.json()["access_token"]

    response = await client.get(
        "/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"
