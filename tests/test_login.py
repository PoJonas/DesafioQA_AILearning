import requests


def test_login_valido(base_url, usuario_cadastrado):
    response = requests.post(f"{base_url}/login", json={
        "email": usuario_cadastrado["email"],
        "password": usuario_cadastrado["password"]
    })
    body = response.json()

    assert response.status_code == 200
    assert "authorization" in body


def test_login_email_invalido(base_url):
    response = requests.post(f"{base_url}/login", json={
        "email": "naoexiste@email.com",
        "password": "teste123"
    })

    assert response.status_code == 401


def test_login_senha_invalida(base_url, usuario_cadastrado):
    response = requests.post(f"{base_url}/login", json={
        "email": usuario_cadastrado["email"],
        "password": "senha_errada"
    })

    assert response.status_code == 401
