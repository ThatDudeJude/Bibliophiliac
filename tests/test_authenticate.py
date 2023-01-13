def test_login_registration_page(client):
    response = client.get("/login")
    assert response.status == "200 OK"
    assert b"Log In" in response.data
    response = client.get("/register")
    assert response.status == "200 OK"
    assert b"Register" in response.data


def test_registration(client, authenticate):
    with client:
        response = authenticate.register(username="test register", password="12345")
        assert response.status == "302 FOUND"
        response = authenticate.login(username="test register", password="12345")
        assert response.status_code == 302


def test_login_logout_redirect(client, authenticate):
    with client:
        response = authenticate.login()
        assert response.status_code == 302
        response = client.get("/search")
        assert response.status == "200 OK"
        assert b"Book" in response.data
        response = authenticate.logout()
        assert response.status_code == 302
        assert b"login" in response.data


def test_logged_account(client, authenticate):
    with client:
        authenticate.login()
        response = client.get("/search")
        assert b"test client" in response.data
        assert b"Book" in response.data
        response = authenticate.logout()
        assert b"login" in response.data
