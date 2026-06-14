import requests
from utils.data_generator import gerar_usuario

# Para verificar a documentação especifica de cada caso de teste, procure pelo arquivo abaixo
# Documentação em: Detalhamento/Testes_Usuarios.md

def test_listar_usuarios(base_url):
    resposta = requests.get(f"{base_url}/usuarios")

    assert resposta.status_code == 200
    assert "usuarios" in resposta.json()


def test_cadastrar_usuario_valido(base_url, usuario):
    resposta = requests.post(f"{base_url}/usuarios", json=usuario)
    body = resposta.json()

    assert resposta.status_code == 201
    assert "_id" in body


def test_cadastrar_email_duplicado(base_url, usuario):
    requests.post(f"{base_url}/usuarios", json=usuario)
    resposta = requests.post(f"{base_url}/usuarios", json=usuario)

    assert resposta.status_code == 400
    assert resposta.json()["message"] == "Este email já está sendo usado"


def test_cadastrar_sem_email(base_url, usuario):
    del usuario["email"]
    resposta = requests.post(f"{base_url}/usuarios", json=usuario)

    assert resposta.status_code == 400


def test_cadastrar_sem_nome(base_url, usuario):
    del usuario["nome"]
    resposta = requests.post(f"{base_url}/usuarios", json=usuario)

    assert resposta.status_code == 400


def test_buscar_usuario_por_id(base_url, usuario_cadastrado):
    user_id = usuario_cadastrado["_id"]
    resposta = requests.get(f"{base_url}/usuarios/{user_id}")

    assert resposta.status_code == 200
    assert resposta.json()["_id"] == user_id


def test_buscar_usuario_inexistente(base_url):
    resposta = requests.get(f"{base_url}/usuarios/123456")

    assert resposta.status_code == 400


def test_atualizar_usuario(base_url, usuario_cadastrado):
    user_id = usuario_cadastrado["_id"]
    novo_usuario = gerar_usuario()
    resposta = requests.put(f"{base_url}/usuarios/{user_id}", json=novo_usuario)

    assert resposta.status_code == 200


def test_excluir_usuario(base_url, usuario_cadastrado):
    user_id = usuario_cadastrado["_id"]
    resposta = requests.delete(f"{base_url}/usuarios/{user_id}")

    assert resposta.status_code == 200


def test_excluir_usuario_inexistente(base_url):
    resposta = requests.delete(f"{base_url}/usuarios/123456")

    assert resposta.status_code == 200
