import requests, pytest
from utils.data_generator import gerar_usuario

# Para verificar a documentação especifica de cada caso de teste, procure pelo arquivo abaixo
# Documentação em: Detalhamento/Testes_Usuarios.md


@pytest.mark.usuarios
class TestUsuarios:
    def test_listar_usuarios(self, base_url):
        resposta = requests.get(f"{base_url}/usuarios")

        assert resposta.status_code == 200
        assert "usuarios" in resposta.json()


    def test_cadastrar_usuario_valido(self, base_url, usuario):
        resposta = requests.post(f"{base_url}/usuarios", json=usuario)
        body = resposta.json()

        assert resposta.status_code == 201
        assert resposta.json()["message"] == "Cadastro realizado com sucesso"
        assert "_id" in body


    def test_cadastrar_email_duplicado(self, base_url, usuario):
        requests.post(f"{base_url}/usuarios", json=usuario)
        resposta = requests.post(f"{base_url}/usuarios", json=usuario)

        assert resposta.status_code == 400
        assert resposta.json()["message"] == "Este email já está sendo usado"


    def test_cadastrar_vazio(self, base_url):
        resposta = requests.post(f"{base_url}/login", json={
            "email": "",
            "password": ""
        })

        assert resposta.status_code == 400

    def test_buscar_usuario_por_id(self, base_url, usuario_cadastrado):
        user_id = usuario_cadastrado["_id"]
        resposta = requests.get(f"{base_url}/usuarios/{user_id}")

        assert resposta.status_code == 200
        assert resposta.json()["_id"] == user_id


    def test_buscar_usuario_inexistente(self, base_url):
        resposta = requests.get(f"{base_url}/usuarios/123456")

        assert resposta.status_code == 400


    def test_atualizar_usuario(self, base_url, usuario_cadastrado):
        user_id = usuario_cadastrado["_id"]
        novo_usuario = gerar_usuario()
        resposta = requests.put(f"{base_url}/usuarios/{user_id}", json=novo_usuario)

        assert resposta.status_code == 200


    def test_excluir_usuario(self, base_url, usuario_cadastrado):
        user_id = usuario_cadastrado["_id"]
        resposta = requests.delete(f"{base_url}/usuarios/{user_id}")

        assert resposta.status_code == 200


    def test_excluir_usuario_inexistente(self, base_url):
        resposta = requests.delete(f"{base_url}/usuarios/123456")

        assert resposta.status_code == 200
