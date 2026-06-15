import requests, pytest

# Para verificar a documentação especifica de cada caso de teste, procure pelo arquivo abaixo
# Documentação em: Detalhamento/Testes_Carrinho.md


@pytest.mark.carrinhos
class TestCarrinhos:
    def test_listar_carrinhos(self, base_url):
        resposta = requests.get(f"{base_url}/carrinhos")

        assert resposta.status_code == 200
        assert "carrinhos" in resposta.json()


    def test_criar_carrinho_valido(self, base_url, token, produto_cadastrado):
        payload = {
            "produtos": [
                {
                    "idProduto": produto_cadastrado["_id"],
                    "quantidade": 1
                }
            ]
        }
        resposta = requests.post(f"{base_url}/carrinhos",json=payload, headers={"Authorization": token})

        assert resposta.status_code == 201
        assert "_id" in resposta.json()


    def test_cancelar_compra(self, base_url, token, produto_cadastrado):
        payload = {
            "produtos": [
                {
                    "idProduto": produto_cadastrado["_id"],
                    "quantidade": 1
                }
            ]
        }
        requests.post(f"{base_url}/carrinhos", json=payload, headers={"Authorization": token})

        resposta = requests.delete(f"{base_url}/carrinhos/cancelar-compra", headers={"Authorization": token})

        assert resposta.status_code == 200
