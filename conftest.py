import pytest
import requests
from utils.data_generator import gerar_usuario, gerar_produto

BASE_URL = "https://compassuol.serverest.dev"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def usuario():
    return gerar_usuario()


@pytest.fixture
def usuario_cadastrado(base_url, usuario):
    resposta = requests.post(f"{base_url}/usuarios", json=usuario)
    _id = resposta.json().get("_id")
    dados = {**usuario, "_id": _id}
    yield dados
    requests.delete(f"{base_url}/usuarios/{_id}")


@pytest.fixture
def produto_cadastrado(base_url, token):
    payload = gerar_produto()
    resposta = requests.post(f"{base_url}/produtos", json=payload, headers={"Authorization": token})
    _id = resposta.json().get("_id")
    dados = {**payload, "_id": _id}
    yield dados
    requests.delete(f"{base_url}/produtos/{_id}", headers={"Authorization": token})


@pytest.fixture
def token(base_url, usuario_cadastrado):
    """Faz login com o usuário cadastrado e retorna o token de autorização."""
    resposta = requests.post(f"{base_url}/login", json={
        "email": usuario_cadastrado["email"],
        "password": usuario_cadastrado["password"]
    })
    return resposta.json().get("authorization")


@pytest.fixture
def token_nao_admin(base_url):
    usuario = gerar_usuario(administrador=False)
    resposta_cadastro = requests.post(f"{base_url}/usuarios", json=usuario)
    _id = resposta_cadastro.json().get("_id")

    resposta_login = requests.post(f"{base_url}/login", json={
        "email": usuario["email"],
        "password": usuario["password"]
    })
    token = resposta_login.json().get("authorization")
    yield token
    requests.delete(f"{base_url}/carrinhos/cancelar-compra", headers={"Authorization": token})
    requests.delete(f"{base_url}/usuarios/{_id}")


@pytest.fixture
def produto_cadastrado(base_url, token):
    """Cadastra um produto e retorna seus dados incluindo o _id."""
    payload = gerar_produto()
    resposta = requests.post(f"{base_url}/produtos",json=payload,headers={"Authorization": token})
    _id = resposta.json().get("_id")

    return {**payload, "_id": _id}


@pytest.fixture
def carrinho_cadastrado(base_url, token, produto_cadastrado):
    payload = {
        "produtos": [
            {
                "idProduto": produto_cadastrado["_id"],
                "quantidade": 1
            }
        ]
    }
    resposta = requests.post(f"{base_url}/carrinhos", json=payload, headers={"Authorization": token})
    _id = resposta.json().get("_id")
    yield {**payload, "_id": _id}
    requests.delete(f"{base_url}/carrinhos/cancelar-compra", headers={"Authorization": token})