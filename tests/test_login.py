import requests, pytest
from jsonschema import validate
from utils.schemas import SCHEMA_LOGIN

# Para verificar a documentação especifica de cada caso de teste, procure pelo arquivo abaixo
# Documentação em: Detalhamento/Testes_Login.md


@pytest.mark.login
class TestLogin:
    def test_login_valido(self, base_url, usuario_cadastrado):
        resposta = requests.post(f"{base_url}/login", json={
            "email": usuario_cadastrado["email"],
            "password": usuario_cadastrado["password"]
        })
        body = resposta.json()

        assert resposta.status_code == 200
        validate(instance=resposta.json(), schema=SCHEMA_LOGIN)


    def test_login_email_invalido(self, base_url, usuario_cadastrado):
        resposta = requests.post(f"{base_url}/login", json={
            "email": "naoexiste@email.com",
            "password": usuario_cadastrado["password"]
        })

        assert resposta.status_code == 401
        assert resposta.json()["message"] == "Email e/ou senha inválidos"


    def test_login_senha_invalida(self, base_url, usuario_cadastrado):
        resposta = requests.post(f"{base_url}/login", json={
            "email": usuario_cadastrado["email"],
            "password": "senha_errada"
        })

        assert resposta.status_code == 401
        assert resposta.json()["message"] == "Email e/ou senha inválidos"

    def test_login_campos_vazios(self, base_url):
        resposta = requests.post(f"{base_url}/login", json={
            "email": "",
            "password": ""
        })

        assert resposta.status_code == 400
