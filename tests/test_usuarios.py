import requests
from utils.data_generator import gerar_usuario


def test_listar_usuarios(base_url):
    response = requests.get(f"{base_url}/usuarios")

    assert response.status_code == 200
    assert "usuarios" in response.json()


def test_cadastrar_usuario_valido(base_url, usuario):
    response = requests.post(f"{base_url}/usuarios", json=usuario)
    body = response.json()

    assert response.status_code == 201
    assert "_id" in body


def test_cadastrar_email_duplicado(base_url, usuario):
    requests.post(f"{base_url}/usuarios", json=usuario)
    response = requests.post(f"{base_url}/usuarios", json=usuario)

    assert response.status_code == 400
    assert response.json()["message"] == "Este email já está sendo usado"


def test_cadastrar_sem_email(base_url, usuario):
    del usuario["email"]
    response = requests.post(f"{base_url}/usuarios", json=usuario)

    assert response.status_code == 400


def test_cadastrar_sem_nome(base_url, usuario):
    del usuario["nome"]
    response = requests.post(f"{base_url}/usuarios", json=usuario)

    assert response.status_code == 400


def test_buscar_usuario_por_id(base_url, usuario_cadastrado):
    user_id = usuario_cadastrado["_id"]
    response = requests.get(f"{base_url}/usuarios/{user_id}")

    assert response.status_code == 200
    assert response.json()["_id"] == user_id


def test_buscar_usuario_inexistente(base_url):
    response = requests.get(f"{base_url}/usuarios/123456")

    assert response.status_code == 400


def test_atualizar_usuario(base_url, usuario_cadastrado):
    user_id = usuario_cadastrado["_id"]
    novo_usuario = gerar_usuario()
    response = requests.put(f"{base_url}/usuarios/{user_id}", json=novo_usuario)

    assert response.status_code == 200


def test_excluir_usuario(base_url, usuario_cadastrado):
    user_id = usuario_cadastrado["_id"]
    response = requests.delete(f"{base_url}/usuarios/{user_id}")

    assert response.status_code == 200


def test_excluir_usuario_inexistente(base_url):
    response = requests.delete(f"{base_url}/usuarios/123456")

    assert response.status_code == 200
