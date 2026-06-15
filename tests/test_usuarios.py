import requests, pytest, random
from utils.data_generator import gerar_usuario

# Para verificar a documentação especifica de cada caso de teste, procure pelo arquivo abaixo
# Documentação em: Detalhamento/Testes_Usuarios.md


@pytest.mark.usuarios
class TestUsuarios:
    def test_listar_usuarios(self, base_url, usuario):
        requests.post(f"{base_url}/usuarios", json=usuario)
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

    def test_cadastrar_validacao_emoji(self, base_url, usuario):
        usuario["email"] = f"teste{random.randint(0, 100000)}😄😄😄@gmail😄😄.com"
        resposta = requests.post(f"{base_url}/usuarios", json=usuario)

        assert resposta.status_code == 201
        assert resposta.json()["message"] == "Cadastro realizado com sucesso"

    def test_cadastrar_campos_vazios(self, base_url):
        resposta = requests.post(f"{base_url}/usuarios", json={
            "nome": "",
            "email": "",
            "password": "",
            "administrador": "true"
        })

        assert resposta.status_code == 400

    def test_buscar_usuario_por_id(self, base_url, usuario_cadastrado):
        user_id = usuario_cadastrado["_id"]
        resposta = requests.get(f"{base_url}/usuarios/{user_id}")

        assert resposta.status_code == 200
        assert resposta.json()["_id"] == user_id


    def test_buscar_usuario_inexistente(self, base_url):
        resposta = requests.get(f"{base_url}/usuarios/0000aaaa1111bbbb")

        assert resposta.status_code == 400
        assert resposta.json()["message"] == "Usuário não encontrado"


    def test_atualizar_usuario(self, base_url, usuario_cadastrado):
        user_id = usuario_cadastrado["_id"]
        novo_usuario = gerar_usuario()
        resposta = requests.put(f"{base_url}/usuarios/{user_id}", json=novo_usuario)

        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Registro alterado com sucesso"


    def test_atualizar_usuario_inexistente(self, base_url):
        novo_usuario = gerar_usuario()
        resposta = requests.put(f"{base_url}/usuarios/0000aaaa1111bbbb", json=novo_usuario)

        assert resposta.status_code == 201
        assert resposta.json()["message"] == "Cadastro realizado com sucesso"
        assert resposta.json()["_id"] != None


    def test_excluir_usuario(self, base_url, usuario_cadastrado):
        user_id = usuario_cadastrado["_id"]
        resposta = requests.delete(f"{base_url}/usuarios/{user_id}")

        assert resposta.status_code == 200


    def test_excluir_usuario_inexistente(self, base_url):
        resposta = requests.delete(f"{base_url}/usuarios/123456")

        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Nenhum registro excluído"

    def test_excluir_usuario_com_carrinho(self, base_url, token, usuario_cadastrado, produto_cadastrado):
        payload = {
            "produtos": [
                {
                    "idProduto": produto_cadastrado["_id"],
                    "quantidade": 1
                }
            ]
        }

        user_id = usuario_cadastrado["_id"]

        requests.post(f"{base_url}/carrinhos", json=payload, headers={"Authorization": token})
        resposta = requests.delete(f"{base_url}/usuarios/{user_id}")

        assert resposta.status_code == 400
        assert resposta.json()["message"] == "Não é permitido excluir usuário com carrinho cadastrado"
