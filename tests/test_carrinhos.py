import requests, pytest
from utils.data_generator import gerar_usuario, gerar_produto

# Para verificar a documentação especifica de cada caso de teste, procure pelo arquivo abaixo
# Documentação em: Detalhamento/Testes_Carrinho.md


@pytest.mark.carrinhos
class TestCarrinhos:
    def test_listar_carrinhos(self, base_url):
        resposta = requests.get(f"{base_url}/carrinhos")

        assert resposta.status_code == 200
        assert "carrinhos" in resposta.json()


    def test_listar_carrinhos_com_parametros_errados(self, base_url):
        resposta = requests.get(f"{base_url}/carrinhos", params={"quantidade": -1})

        assert resposta.status_code == 400


    def test_criar_carrinho_valido(self, carrinho_cadastrado):
        assert carrinho_cadastrado["_id"] is not None

    def test_criar_carrinho_sem_token(self, base_url, produto_cadastrado):
        payload = {
            "produtos": [
                {
                    "idProduto": produto_cadastrado["_id"],
                    "quantidade": 1
                }
            ]
        }
        resposta = requests.post(f"{base_url}/carrinhos", json=payload)

        assert resposta.status_code == 401
        assert resposta.json()["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


    def test_criar_carrinho_token_nao_admin(self, base_url, produto_cadastrado, token_nao_admin):
        payload = {
            "produtos": [
                {
                    "idProduto": produto_cadastrado["_id"],
                    "quantidade": 1
                }
            ]
        }
        resposta = requests.post(f"{base_url}/carrinhos", json=payload, headers={"Authorization": token_nao_admin})

        assert resposta.status_code == 201
        assert "_id" in resposta.json()


    def test_criar_segundo_carrinho(self, base_url, token, carrinho_cadastrado):
        payload = {
            "produtos": [
                {
                    "idProduto": carrinho_cadastrado["produtos"][0]["idProduto"],
                    "quantidade": 1
                }
            ]
        }
        resposta = requests.post(f"{base_url}/carrinhos", json=payload, headers={"Authorization": token})

        assert resposta.status_code == 400
        assert resposta.json()["message"] == "Não é permitido ter mais de 1 carrinho"


    def test_criar_carrinho_com_produto_duplicado(self, base_url, token, produto_cadastrado):
        produto_id = produto_cadastrado["_id"]
        payload = {
            "produtos": [
                {"idProduto": produto_id, "quantidade": 1},
                {"idProduto": produto_id, "quantidade": 2}
            ]
        }
        resposta = requests.post(f"{base_url}/carrinhos", json=payload, headers={"Authorization": token})

        assert resposta.status_code == 400
        assert resposta.json()["message"] == "Não é permitido possuir produto duplicado"


    def test_criar_carrinho_produto_inexistente(self, base_url, token):
        payload = {
            "produtos": [
                {
                    "idProduto": "0000aaaa1111bbbb",
                    "quantidade": 1
                }
            ]
        }
        resposta = requests.post(f"{base_url}/carrinhos", json=payload, headers={"Authorization": token})

        assert resposta.status_code == 400
        assert resposta.json()["message"] == "Produto não encontrado"


    def test_criar_carrinho_produto_qtd_invalida(self, base_url, token, produto_cadastrado):
        payload = {
            "produtos": [
                {
                    "idProduto": produto_cadastrado["_id"],
                    "quantidade": 0
                }
            ]
        }
        resposta = requests.post(f"{base_url}/carrinhos", json=payload, headers={"Authorization": token})

        assert resposta.status_code == 400


    def test_buscar_carrinho_por_id(self, base_url, carrinho_cadastrado):
        carrinho_id = carrinho_cadastrado["_id"]
        resposta = requests.get(f"{base_url}/carrinhos/{carrinho_id}")

        assert resposta.status_code == 200
        assert resposta.json()["_id"] == carrinho_id


    def test_buscar_carrinho_id_inexistente(self, base_url):
        resposta = requests.get(f"{base_url}/carrinhos/0000aaaa1111bbbb")

        assert resposta.status_code == 400
        assert resposta.json()["message"] == "Carrinho não encontrado"


    def test_fechar_carrinho(self, base_url, token, carrinho_cadastrado):

        resposta = requests.delete(f"{base_url}/carrinhos/concluir-compra", headers={"Authorization": token})

        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Registro excluído com sucesso"


    def test_fechar_carrinho_token_nao_admin(self, base_url, produto_cadastrado, token_nao_admin):
        payload = {
            "produtos": [{"idProduto": produto_cadastrado["_id"], "quantidade": 1}]
        }
        resposta_criacao = requests.post(f"{base_url}/carrinhos", json=payload, headers={"Authorization": token_nao_admin})
        print(resposta_criacao.json())  # ← ver o que está retornando

        resposta = requests.delete(f"{base_url}/carrinhos/concluir-compra", headers={"Authorization": token_nao_admin})

        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Registro excluído com sucesso"


    def test_fechar_carrinho_usuario_sem_carrinho(self, base_url, token):

        requests.delete(f"{base_url}/carrinhos/cancelar-compra", headers={"Authorization": token})
        resposta = requests.delete(f"{base_url}/carrinhos/concluir-compra", headers={"Authorization": token})

        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Não foi encontrado carrinho para esse usuário"


    def test_cancelar_compra(self, base_url, token, carrinho_cadastrado):

        resposta = requests.delete(f"{base_url}/carrinhos/cancelar-compra", headers={"Authorization": token})

        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Registro excluído com sucesso. Estoque dos produtos reabastecido"


    def test_cancelar_compra_token_nao_admin(self, base_url, produto_cadastrado, token_nao_admin):
        payload = {
            "produtos": [
                {
                    "idProduto": produto_cadastrado["_id"],
                    "quantidade": 1
                }
            ]
        }
        requests.post(f"{base_url}/carrinhos", json=payload, headers={"Authorization": token_nao_admin})
        resposta = requests.delete(f"{base_url}/carrinhos/cancelar-compra", headers={"Authorization": token_nao_admin})

        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Registro excluído com sucesso. Estoque dos produtos reabastecido"


    def test_cancelar_compra_usuario_sem_carrinho(self, base_url, token):

        requests.delete(f"{base_url}/carrinhos/cancelar-compra", headers={"Authorization": token})
        resposta = requests.delete(f"{base_url}/carrinhos/cancelar-compra", headers={"Authorization": token})

        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Não foi encontrado carrinho para esse usuário"
