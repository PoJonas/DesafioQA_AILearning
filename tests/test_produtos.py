import requests, pytest
from utils.data_generator import gerar_produto

# Para verificar a documentação especifica de cada caso de teste, procure pelo arquivo abaixo
# Documentação em: Detalhamento/Testes_Produtos.md


@pytest.mark.produtos
class TestProdutos:
    def test_listar_produtos(self, base_url):
        resposta = requests.get(f"{base_url}/produtos")

        assert resposta.status_code == 200
        assert "produtos" in resposta.json()


    def test_cadastrar_produto_valido(self, base_url, token):
        payload = gerar_produto()
        resposta = requests.post(f"{base_url}/produtos",json=payload, headers={"Authorization": token})
        body = resposta.json()

        assert resposta.status_code == 201
        assert "_id" in body


    def test_cadastrar_produto_sem_token(self, base_url):
        payload = gerar_produto()
        resposta = requests.post(f"{base_url}/produtos", json=payload)

        assert resposta.status_code == 401


    def test_buscar_produto_por_id(self, base_url, produto_cadastrado):
        produto_id = produto_cadastrado["_id"]
        resposta = requests.get(f"{base_url}/produtos/{produto_id}")

        assert resposta.status_code == 200
        assert resposta.json()["_id"] == produto_id


    def test_excluir_produto(self, base_url, token, produto_cadastrado):
        produto_id = produto_cadastrado["_id"]
        resposta = requests.delete(f"{base_url}/produtos/{produto_id}", headers={"Authorization": token})

        assert resposta.status_code == 200
