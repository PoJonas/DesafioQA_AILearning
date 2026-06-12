import requests


def test_listar_carrinhos(base_url):
    resposta = requests.get(f"{base_url}/carrinhos")

    assert resposta.status_code == 200
    assert "carrinhos" in resposta.json()


def test_cadastrar_carrinho(base_url, token, produto_cadastrado):
    payload = {
        "produtos": [
            {
                "idProduto": produto_cadastrado["_id"],
                "quantidade": 1
            }
        ]
    }
    resposta = requests.post(f"{base_url}/carrinhos",json=payload,headers={"Authorization": token})
    assert resposta.status_code == 201
    assert "_id" in resposta.json()


def test_cancelar_compra(base_url, token, produto_cadastrado):
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
