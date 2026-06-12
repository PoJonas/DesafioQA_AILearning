import requests


def test_listar_carrinhos(base_url):
    response = requests.get(f"{base_url}/carrinhos")

    assert response.status_code == 200
    assert "carrinhos" in response.json()


def test_cadastrar_carrinho(base_url, token, produto_cadastrado):
    payload = {
        "produtos": [
            {
                "idProduto": produto_cadastrado["_id"],
                "quantidade": 1
            }
        ]
    }
    response = requests.post(
        f"{base_url}/carrinhos",
        json=payload,
        headers={"Authorization": token}
    )

    assert response.status_code == 201
    assert "_id" in response.json()


def test_cancelar_compra(base_url, token, produto_cadastrado):
    payload = {
        "produtos": [
            {
                "idProduto": produto_cadastrado["_id"],
                "quantidade": 1
            }
        ]
    }
    requests.post(
        f"{base_url}/carrinhos",
        json=payload,
        headers={"Authorization": token}
    )

    response = requests.delete(
        f"{base_url}/carrinhos/cancelar-compra",
        headers={"Authorization": token}
    )

    assert response.status_code == 200
