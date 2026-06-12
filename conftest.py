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
    """Cria um usuário na API e retorna seus dados incluindo o _id."""
    resposta = requests.post(f"{base_url}/usuarios", json=usuario)
    _id = resposta.json().get("_id")
    return {**usuario, "_id": _id}


@pytest.fixture
def token(base_url, usuario_cadastrado):
    """Faz login com o usuário cadastrado e retorna o token de autorização."""
    resposta = requests.post(f"{base_url}/login", json={
        "email": usuario_cadastrado["email"],
        "password": usuario_cadastrado["password"]
    })
    return resposta.json().get("authorization")


@pytest.fixture
def produto_cadastrado(base_url, token):
    """Cadastra um produto e retorna seus dados incluindo o _id."""
    payload = gerar_produto()
    resposta = requests.post(
        f"{base_url}/produtos",
        json=payload,
        headers={"Authorization": token}
    )
    _id = resposta.json().get("_id")
    return {**payload, "_id": _id}
