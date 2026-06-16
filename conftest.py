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
    resposta = requests.post(f"{base_url}/usuarios", json=usuario) # cadastra um usuario e guarda seus dados
    _id = resposta.json().get("_id")
    dados = {**usuario, "_id": _id}
    yield dados
    requests.delete(f"{base_url}/usuarios/{_id}")  # cleanup automático após cada teste


@pytest.fixture
def token(base_url, usuario_cadastrado):
    resposta = requests.post(f"{base_url}/login", json={  # usa a fixture 'usuario'cadastrado' e faz login usando ela
        "email": usuario_cadastrado["email"],
        "password": usuario_cadastrado["password"]
    })
    return resposta.json().get("authorization")


@pytest.fixture
def token_nao_admin(base_url):   # Mesmo principio do token normal mas com administrador=False
    usuario = gerar_usuario(administrador=False)
    resposta_cadastro = requests.post(f"{base_url}/usuarios", json=usuario)
    _id = resposta_cadastro.json().get("_id")

    resposta_login = requests.post(f"{base_url}/login", json={
        "email": usuario["email"],
        "password": usuario["password"]
    })
    token = resposta_login.json().get("authorization")
    yield token
    # cancela carrinho antes de deletar o usuário - a API bloqueia exclusão de usuário com carrinho ativo
    # Ajuste necessário pois a fixture cria um usuario dentro dela
    requests.delete(f"{base_url}/carrinhos/cancelar-compra", headers={"Authorization": token})
    requests.delete(f"{base_url}/usuarios/{_id}") # cleanup


@pytest.fixture
def produto_cadastrado(base_url, token):
    payload = gerar_produto()
    resposta = requests.post(f"{base_url}/produtos", json=payload, headers={"Authorization": token})
    _id = resposta.json().get("_id")     
    dados = {**payload, "_id": _id}
    yield dados
    # tenta deletar — pode falhar silenciosamente se o produto ainda estiver em um carrinho ativo
    requests.delete(f"{base_url}/produtos/{_id}", headers={"Authorization": token}) # cleanup


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
    
    # se o carrinho não foi criado, aborta com mensagem clara
    assert _id is not None, f"Falha ao criar carrinho na fixture. Resposta: {resposta.json()}"
    
    yield {**payload, "_id": _id}
    # cancelar-compra é usado no lugar de DELETE direto pois reabastece o estoque do produto
    requests.delete(f"{base_url}/carrinhos/cancelar-compra", headers={"Authorization": token}) # cleanup
