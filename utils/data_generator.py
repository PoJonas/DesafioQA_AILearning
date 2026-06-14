from faker import Faker # Import da biblioteca Faker para geração da massa de dados dos testes
import random

fake = Faker("pt_BR") # Define a linguagem utilizada pelos dados gerados

# Retorna um Dict contendo os dados necessários para o cadastro de um novo usuário seguindo o padrão de schema da ServerRest
def gerar_usuario(): 
    return {
        "nome": fake.name(),
        "email": fake.email(),
        "password": "teste123",
        "administrador": "true"
    }

def gerar_produto():
    return {      
        "nome": fake.random_company_product(),
        "preco": random.randint(),
        "descricao": fake.random_company_product(),
        "quantidade": random.randint()
    }
