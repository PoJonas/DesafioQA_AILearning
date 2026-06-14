import requests, pytest

# Para verificar a documentação especifica de cada caso de teste, procure pelo arquivo abaixo
# Documentação em: Detalhamento/Testes_Carrinho.md


@pytest.mark.carrinhos
class TestCarrinhos:
    def test_listar_carrinhos(self, base_url):
        response = requests.get(f"{base_url}/carrinhos")

        assert response.status_code == 200
        assert "carrinhos" in response.json()


    def test_criar_carrinho_valido(self, base_url, token, produto_cadastrado):
        payload = {
            "produtos": [
                {
                    "idProduto": produto_cadastrado["_id"],
                    "quantidade": 1
                }
            ]
        }
        response = requests.post(f"{base_url}/carrinhos",json=payload, headers={"Authorization": token})

        assert response.status_code == 201
        assert "_id" in response.json()


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

        response = requests.delete(f"{base_url}/carrinhos/cancelar-compra", headers={"Authorization": token})

        assert response.status_code == 200
