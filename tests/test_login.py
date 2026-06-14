import requests, pytest

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
        assert "authorization" in body


    def test_login_email_invalido(self, base_url):
        resposta = requests.post(f"{base_url}/login", json={
            "email": "naoexiste@email.com",
            "password": "teste123"
        })

        assert resposta.status_code == 401


    def test_login_senha_invalida(self, base_url, usuario_cadastrado):
        resposta = requests.post(f"{base_url}/login", json={
            "email": usuario_cadastrado["email"],
            "password": "senha_errada"
        })

        assert resposta.status_code == 401
