# Desafio QA — AI/R Learning

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

- Os dados de usuário são gerados dinamicamente via `faker` a cada execução e estão definidas em `utils/data_generator`.
- As fixtures globais estão definidas no `conftest.py` e ficam disponíveis para todos os testes automaticamente.

---

## Descrição dos testes

Os testes estão organizados por endpoint em arquivos separados dentro de `tests/`.

**`test_usuarios.py`** — endpoint `/usuarios`
**`test_login.py`** — endpoint `/login`
**`test_produtos.py`** — endpoint `/produtos`
**`test_carrinhos.py`** — endpoint `/carrinhos`

Para verificar detalhamente cada um dos casos de testes acesse suas documentações individuais em `Detalhamento/`.