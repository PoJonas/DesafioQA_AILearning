import requests
from utils.data_generator import gerar_produto


def test_listar_produtos(base_url):
    response = requests.get(f"{base_url}/produtos")

    assert response.status_code == 200
    assert "produtos" in response.json()


def test_cadastrar_produto_valido(base_url, token):
    payload = gerar_produto()
    response = requests.post(
        f"{base_url}/produtos",
        json=payload,
        headers={"Authorization": token}
    )
    body = response.json()

    assert response.status_code == 201
    assert "_id" in body


def test_cadastrar_produto_sem_autorizacao(base_url):
    payload = gerar_produto()
    response = requests.post(f"{base_url}/produtos", json=payload)

    assert response.status_code == 401


def test_buscar_produto_por_id(base_url, produto_cadastrado):
    produto_id = produto_cadastrado["_id"]
    response = requests.get(f"{base_url}/produtos/{produto_id}")

    assert response.status_code == 200
    assert response.json()["_id"] == produto_id


def test_excluir_produto(base_url, token, produto_cadastrado):
    produto_id = produto_cadastrado["_id"]
    response = requests.delete(
        f"{base_url}/produtos/{produto_id}",
        headers={"Authorization": token}
    )

    assert response.status_code == 200
