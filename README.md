# DesafioQA — AI Learning

Projeto de automação de testes de API desenvolvido como desafio de QA, utilizando Python e Pytest contra a API [ServeRest](https://serverest.dev) hospedada pela CompassUOL.

---

## Tecnologias

| Ferramenta | Versão  | Uso                          |
|------------|---------|------------------------------|
| Python     | 3.x     | Linguagem principal          |
| pytest     | 9.0.3   | Framework de testes          |
| requests   | 2.34.2  | Requisições HTTP             |
| faker      | 40.23.0 | Geração de dados dinâmicos   |

---

## Estrutura do projeto

```
DesafioQA_AILearning/
├── tests/          # Casos de teste
├── utils/          # Utilitários (gerador de dados, helpers)
├── conftest.py     # Fixtures globais do pytest
├── requirements.txt
└── README.md
```

---

## Instalação e execução

**1. Clone o repositório**
```bash
git clone https://github.com/PoJonas/DesafioQA_AILearning.git
cd DesafioQA_AILearning
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Execute os testes**
```bash
python -m pytest
```

Para ver mais detalhes na saída:
```bash
python -m pytest -v
```

---

## API alvo

Os testes são executados contra a instância CompassUOL do ServeRest:

```
https://compassuol.serverest.dev
```

> A documentação completa dos endpoints está disponível em [serverest.dev](https://serverest.dev).

---

## Observações

- Os dados de usuário são gerados dinamicamente via `faker` a cada execução.
- As fixtures globais (`usuario`, `base_url`) estão definidas no `conftest.py` e ficam disponíveis para todos os testes automaticamente.

---

## Descrição dos testes

Os testes estão organizados por endpoint em arquivos separados dentro de `tests/`.

**`test_usuarios.py`** — endpoint `/usuarios`

| Teste | Método | Cenário |
|---|---|---|
| `test_listar_usuarios` | GET | Listagem retorna status 200 e o campo `usuarios` |
| `test_cadastrar_usuario_valido` | POST | Cadastro com dados válidos retorna status 201 e um `_id` |
| `test_cadastrar_email_duplicado` | POST | E-mail já existente retorna status 400 |
| `test_cadastrar_sem_email` | POST | Cadastro sem o campo `email` retorna status 400 |
| `test_cadastrar_sem_nome` | POST | Cadastro sem o campo `nome` retorna status 400 |
| `test_buscar_usuario_por_id` | GET | Busca por ID retorna o usuário correto com status 200 |
| `test_buscar_usuario_inexistente` | GET | ID inválido retorna status 400 |
| `test_atualizar_usuario` | PUT | Atualização de usuário existente retorna status 200 |
| `test_excluir_usuario` | DELETE | Exclusão de usuário existente retorna status 200 |
| `test_excluir_usuario_inexistente` | DELETE | Exclusão de ID inexistente retorna status 200 |

**`test_login.py`** — endpoint `/login`

| Teste | Método | Cenário |
|---|---|---|
| `test_login_valido` | POST | Credenciais válidas retornam status 200 e o token de autorização |
| `test_login_email_invalido` | POST | E-mail inexistente retorna status 401 |
| `test_login_senha_invalida` | POST | Senha incorreta retorna status 401 |

**`test_produtos.py`** — endpoint `/produtos`

| Teste | Método | Cenário |
|---|---|---|
| `test_listar_produtos` | GET | Listagem retorna status 200 e o campo `produtos` |
| `test_cadastrar_produto_valido` | POST | Cadastro autenticado retorna status 201 e um `_id` |
| `test_cadastrar_produto_sem_autorizacao` | POST | Cadastro sem token retorna status 401 |
| `test_buscar_produto_por_id` | GET | Busca por ID retorna o produto correto com status 200 |
| `test_excluir_produto` | DELETE | Exclusão autenticada retorna status 200 |

**`test_carrinhos.py`** — endpoint `/carrinhos`

| Teste | Método | Cenário |
|---|---|---|
| `test_listar_carrinhos` | GET | Listagem retorna status 200 e o campo `carrinhos` |
| `test_cadastrar_carrinho` | POST | Criação de carrinho autenticada retorna status 201 e um `_id` |
| `test_cancelar_compra` | DELETE | Cancelamento de compra retorna status 200 |
