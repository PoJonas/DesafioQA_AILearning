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
