from faker import Faker
import random

fake = Faker("pt_BR")


def gerar_usuario():
    return {
        "nome": fake.name(),
        "email": fake.email(),
        "password": "teste123",
        "administrador": "true"
    }


def gerar_produto():
    return {
        "nome": fake.word().capitalize() + " " + fake.word().capitalize(),
        "preco": random.randint(10, 500),
        "descricao": fake.sentence(),
        "quantidade": random.randint(1, 100)
    }
