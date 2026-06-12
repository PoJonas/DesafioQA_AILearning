from faker import Faker

fake = Faker()

def gerar_usuario():
    return {
        "nome": fake.name(),
        "email": fake.email(),
        "password": "teste123",
        "administrador": "true"
    }