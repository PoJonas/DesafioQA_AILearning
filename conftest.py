import pytest
import requests
from utils.data_generator import gerar_usuario

BASE_URL = "https://compassuol.serverest.dev"


# Fixtures principais utilizadas

# Retorna a URL base, definida previamente na variavel 'BASE_URL'
@pytest.fixture
def base_url():
    return BASE_URL

# Retorna a execução da função 'gerar_usuario()', armazenada no arquivo 'data_generator.py' dentro da pasta utils
@pytest.fixture
def usuario():
    return gerar_usuario()


# Recebe como parametro as duas Fixtures anteriores e usa seus dados para cadastrar um novo usuário na API
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