from faker import Faker # Import da biblioteca Faker para geração da massa de dados dos testes
import random

fake = Faker("pt_BR") # Define a linguagem utilizada pelos dados gerados

# Retorna um Dict contendo os dados necessários para o cadastro de um novo usuário seguindo o padrão de schema da ServerRest
def gerar_usuario(administrador: bool = True):
    return {
        "nome": fake.name(),
        "email": fake.email(),
        "password": "teste123",
        "administrador": str(administrador).lower()
    }

# Retorna um Dict com os dados de um produto simulado seguindo o padrão de schema da ServerRest
def gerar_produto():
    return {
        "nome": fake.unique.bothify(text="Produto ???-###"), # Gera valores seguindo o padrão 'Produto ABC-123'
        "preco": random.randint(1, 1000),
        "descricao": fake.sentence(nb_words=6), # Gera uma frase com 6 palavras
        "quantidade": random.randint(0, 100)
    }
