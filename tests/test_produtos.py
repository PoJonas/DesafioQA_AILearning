import requests, pytest
from utils.data_generator import gerar_produto
from jsonschema import validate
from utils.schemas import SCHEMA_LISTAR_PRODUTOS, SCHEMA_PRODUTO

# Para verificar a documentação especifica de cada caso de teste, procure pelo arquivo abaixo
# Documentação em: Detalhamento/Testes_Produtos.md


@pytest.mark.produtos
class TestProdutos:
    def test_listar_produtos(self, base_url):

        resposta = requests.get(f"{base_url}/produtos")

        assert resposta.status_code == 200
        validate(instance=resposta.json(), schema=SCHEMA_LISTAR_PRODUTOS)


    def test_cadastrar_produto_valido(self, base_url, token):

        payload = gerar_produto()
        resposta = requests.post(f"{base_url}/produtos", json=payload, headers={"Authorization": token})
        body = resposta.json()

        assert resposta.status_code == 201
        assert "_id" in body


    def test_cadastrar_produto_sem_token(self, base_url):

        payload = gerar_produto()
        resposta = requests.post(f"{base_url}/produtos", json=payload)

        assert resposta.status_code == 401
        assert resposta.json()["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


    def test_cadastrar_produto_token_nao_admin(self, base_url, token_nao_admin):

        payload = gerar_produto()
        resposta = requests.post(f"{base_url}/produtos", json=payload, headers={"Authorization": token_nao_admin})

        assert resposta.status_code == 403
        assert resposta.json()["message"] == "Rota exclusiva para administradores"


    def test_cadastrar_produto_nome_duplicado(self, base_url, token, produto_cadastrado):

        payload = gerar_produto()
        payload["nome"] = produto_cadastrado["nome"]
        resposta = requests.post(f"{base_url}/produtos", json=payload, headers={"Authorization": token})

        assert resposta.status_code == 400
        assert resposta.json()["message"] == "Já existe produto com esse nome"


    def test_cadastrar_produto_campo_ausente(self, base_url, token):

        payload = gerar_produto()
        del payload["preco"]
        resposta = requests.post(f"{base_url}/produtos", json=payload, headers={"Authorization": token})

        assert resposta.status_code == 400
        assert "preco" in resposta.json()


    def test_cadastrar_produto_preco_invalido(self, base_url, token):

        payload = gerar_produto()
        payload["preco"] = -1
        resposta = requests.post(f"{base_url}/produtos", json=payload, headers={"Authorization": token})

        assert resposta.status_code == 400


    def test_buscar_produto_por_id(self, base_url, produto_cadastrado):

        produto_id = produto_cadastrado["_id"]
        resposta = requests.get(f"{base_url}/produtos/{produto_id}")

        assert resposta.status_code == 200
        validate(instance=resposta.json(), schema=SCHEMA_PRODUTO)


    def test_buscar_produto_inexistente(self, base_url):

        resposta = requests.get(f"{base_url}/produtos/0000aaaa1111bbbb")

        assert resposta.status_code == 400
        assert resposta.json()["message"] == "Produto não encontrado"


    def test_atualizar_produto(self, base_url, token, produto_cadastrado):

        produto_id = produto_cadastrado["_id"]
        payload_atualizado = gerar_produto()
        resposta = requests.put(f"{base_url}/produtos/{produto_id}", json=payload_atualizado, headers={"Authorization": token})

        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Registro alterado com sucesso"


    def test_atualizar_produto_sem_token(self, base_url, produto_cadastrado):

        produto_id = produto_cadastrado["_id"]
        payload_atualizado = gerar_produto()
        resposta = requests.put(f"{base_url}/produtos/{produto_id}", json=payload_atualizado)

        assert resposta.status_code == 401
        assert resposta.json()["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


    def test_atualizar_produto_token_nao_admin(self, base_url, produto_cadastrado, token_nao_admin):

        produto_id = produto_cadastrado["_id"]
        payload_atualizado = gerar_produto()
        resposta = requests.put(f"{base_url}/produtos/{produto_id}", json=payload_atualizado, headers={"Authorization": token_nao_admin})

        assert resposta.status_code == 403
        assert resposta.json()["message"] == "Rota exclusiva para administradores"


    def test_atualizar_produto_inexistente(self, base_url, token):
        # Produto com ID inexistente deve ser criado (comportamento upsert da API)
        payload = gerar_produto()
        resposta = requests.put(f"{base_url}/produtos/0000aaaa1111bbbb", json=payload, headers={"Authorization": token})

        assert resposta.status_code == 201
        assert resposta.json()["message"] == "Cadastro realizado com sucesso"
        assert resposta.json()["_id"] is not None


    def test_atualizar_produto_nome_duplicado(self, base_url, token, produto_cadastrado):
        # Cria um segundo produto para ter um nome de referência
        segundo_produto = gerar_produto()
        resposta_criacao = requests.post(f"{base_url}/produtos", json=segundo_produto, headers={"Authorization": token})
        segundo_id = resposta_criacao.json().get("_id")

        # Tenta renomear o segundo produto com o nome do primeiro
        payload_atualizado = gerar_produto()
        payload_atualizado["nome"] = produto_cadastrado["nome"]
        resposta = requests.put(f"{base_url}/produtos/{segundo_id}", json=payload_atualizado, headers={"Authorization": token})

        assert resposta.status_code == 400
        assert resposta.json()["message"] == "Já existe produto com esse nome"


    def test_excluir_produto(self, base_url, token, produto_cadastrado):

        produto_id = produto_cadastrado["_id"]
        resposta = requests.delete(f"{base_url}/produtos/{produto_id}", headers={"Authorization": token})

        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Registro excluído com sucesso"


    def test_excluir_produto_sem_token(self, base_url, produto_cadastrado):

        produto_id = produto_cadastrado["_id"]
        resposta = requests.delete(f"{base_url}/produtos/{produto_id}")

        assert resposta.status_code == 401
        assert resposta.json()["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


    def test_excluir_produto_token_nao_admin(self, base_url, produto_cadastrado, token_nao_admin):

        produto_id = produto_cadastrado["_id"]
        resposta = requests.delete(f"{base_url}/produtos/{produto_id}", headers={"Authorization": token_nao_admin})

        assert resposta.status_code == 403
        assert resposta.json()["message"] == "Rota exclusiva para administradores"


    def test_excluir_produto_no_carrinho(self, base_url, token, produto_cadastrado):
        # Adiciona o produto ao carrinho do usuário admin
        payload_carrinho = {
            "produtos": [
                {
                    "idProduto": produto_cadastrado["_id"],
                    "quantidade": 1
                }
            ]
        }
        requests.post(f"{base_url}/carrinhos", json=payload_carrinho, headers={"Authorization": token})

        # Tenta excluir o produto que está no carrinho
        produto_id = produto_cadastrado["_id"]
        resposta = requests.delete(f"{base_url}/produtos/{produto_id}", headers={"Authorization": token})

        assert resposta.status_code == 400
        assert "carrinho" in resposta.json()["message"].lower()