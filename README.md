# DesafioQA — AI/R Learning

> Suíte de testes automatizados para a API [ServeRest](https://serverest.dev), desenvolvida como parte do programa de aprendizado AI/R Learning da CompassUOL.

---

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como executar](#como-executar)
- [Cobertura de testes](#cobertura-de-testes)
- [Extras implementados](#extras-implementados)
- [Bugs identificados](#bugs-identificados)

---

## Sobre o projeto

Este projeto valida o comportamento da API ServeRest nos seus quatro endpoints principais (`/usuarios`, `/login`, `/produtos`, `/carrinhos`), cobrindo fluxos positivos, negativos e regras de negócio críticas.

A suíte foi construída de forma incremental, com foco em:

- Independência entre os testes
- Dados dinâmicos gerados via Faker
- Fixtures reutilizáveis com setup e teardown
- Validação de contrato via JSON Schema
- CI/CD com GitHub Actions

---

## Tecnologias

| Ferramenta | Versão | Uso |
|---|---|---|
| Python | 3.x | Linguagem principal |
| pytest | 9.0.3 | Framework de testes |
| requests | 2.34.2 | Requisições HTTP |
| Faker | 40.23.0 | Geração de dados dinâmicos |
| jsonschema | 4.26.0 | Validação de contrato |

---

## Estrutura do projeto

```
DesafioQA_AILearning/
├── .github/
│   └── workflows/
│       └── testes.yml          # GitHub Actions
├── tests/
│   ├── conftest.py             # Fixtures globais
│   ├── test_usuarios.py
│   ├── test_login.py
│   ├── test_produtos.py
│   └── test_carrinhos.py
├── utils/
│   ├── data_generator.py       # Geração de dados com Faker
│   └── schemas.py              # JSON Schemas para validação de contrato
├── Detalhamento/
│   ├── Testes_Usuarios.md
│   ├── Testes_Login.md
│   ├── Testes_Produtos.md
│   └── Testes_Carrinho.md
├── PLANO-DE-TESTES.md
├── requirements.txt
└── pytest.ini
```

---

## Como executar

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/DesafioQA_AILearning.git
cd DesafioQA_AILearning
```

**2. Crie e ative um ambiente virtual**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Execute os testes**
```bash
# Todos os testes
python -m pytest -v

# Por endpoint
python -m pytest -v -m usuarios
python -m pytest -v -m login
python -m pytest -v -m produtos
python -m pytest -v -m carrinhos
```

---

## Cobertura de testes

A cobertura foi calculada com base na metodologia descrita no artigo [Como verificar a cobertura de testes da API REST](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b), que utiliza critérios de cobertura de entrada (Input Coverage) e saída (Output Coverage).

### Critérios e resultados

**Path Coverage** — verifica se todos os endpoints únicos da API estão cobertos.

```
Endpoints cobertos / Total de endpoints = 9 / 9 = 100%
```

**Operator Coverage** — verifica se todos os métodos HTTP de cada endpoint estão cobertos.

```
Operações cobertas / Total de operações = 16 / 16 = 100%
```

| Endpoint | Métodos cobertos |
|---|---|
| `POST /login` | ✅ |
| `GET /usuarios` | ✅ |
| `POST /usuarios` | ✅ |
| `GET /usuarios/{_id}` | ✅ |
| `PUT /usuarios/{_id}` | ✅ |
| `DELETE /usuarios/{_id}` | ✅ |
| `GET /produtos` | ✅ |
| `POST /produtos` | ✅ |
| `GET /produtos/{_id}` | ✅ |
| `PUT /produtos/{_id}` | ✅ |
| `DELETE /produtos/{_id}` | ✅ |
| `GET /carrinhos` | ✅ |
| `POST /carrinhos` | ✅ |
| `GET /carrinhos/{_id}` | ✅ |
| `DELETE /carrinhos/concluir-compra` | ✅ |
| `DELETE /carrinhos/cancelar-compra` | ✅ |

**Status Code Coverage** — verifica se todos os status codes documentados no swagger estão cobertos.

```
Status codes cobertos / Total documentado = 33 / 33 = 100%
```

**Parameter Value Coverage** — verifica se todos os valores possíveis de parâmetros enum e booleanos estão cobertos. A API possui o campo `administrador` com enum `["true", "false"]`, e ambos os valores são testados.

```
Valores cobertos / Total de valores possíveis = 2 / 2 = 100%
```

**Response Properties Body Coverage** — verifica se todos os campos das respostas estão sendo validados. Os endpoints GET têm contrato validado via JSON Schema, cobrindo todos os campos documentados no swagger.

```
Cobertura = 100%
```

### Resumo

| Critério | Resultado |
|---|---|
| Path Coverage | 100% (9/9) |
| Operator Coverage | 100% (16/16) |
| Status Code Coverage | 100% (33/33) |
| Parameter Value Coverage | 100% (2/2) |
| Response Properties Body Coverage | 100% |

---

## Extras implementados

### Extra 1 — Validação de contrato com JSON Schema

Todos os endpoints GET têm a estrutura da resposta validada via JSON Schema, garantindo que campos obrigatórios, tipos e valores enum estão corretos. Os schemas estão centralizados em `utils/schemas.py` e foram construídos com base no swagger oficial da ServeRest.

Endpoints com validação de contrato:

- `GET /usuarios` — `SCHEMA_LISTAR_USUARIOS`
- `GET /usuarios/{_id}` — `SCHEMA_USUARIO`
- `POST /login` — `SCHEMA_LOGIN`
- `GET /produtos` — `SCHEMA_LISTAR_PRODUTOS`
- `GET /produtos/{_id}` — `SCHEMA_PRODUTO`
- `GET /carrinhos` — `SCHEMA_LISTAR_CARRINHOS`
- `GET /carrinhos/{_id}` — `SCHEMA_CARRINHO`

### Extra 2 — GitHub Actions

A suíte é executada automaticamente a cada push na branch `main` via GitHub Actions. A configuração está em `.github/workflows/testes.yml`.

---

## Bugs identificados

Os bugs encontrados durante a execução foram reportados como issues no repositório. Abaixo um resumo:

| # | Endpoint | Descrição | Severidade |
|---|---|---|---|
| 1 | `GET /usuarios` | Retorna senha dos usuários em texto plano | Crítica |
| 2 | `POST /usuarios` | Aceita emojis no corpo e domínio do email sem validação | Alta |
| 3 | `GET /usuarios/{_id}` | Retorna senha do usuário em texto plano | Crítica |
| 4 | `GET /usuarios/{_id}` | A documentação não menciona que o ID precisa ter exatamente 16 caracteres alfanuméricos | Baixa |
| 5 | `POST /produtos` | Pode ser colocado qualquer valor no campo de `preco`, podendo estourar o limite do tipo integer | Média |


> Para detalhes completos de cada bug (passos para reproduzir, resultado esperado, resultado obtido e evidências), consulte a aba **Issues** do repositório.


## Agradecimentos

E por último mas não menos importante, quero agradecer a todos que me ajudaram a chegar até o fim desse bootcamp: A minha amiga Andressa que me incentivou a se inscrever mesmo eu achando que não seria selecionado, aos meus colegas de squad que me ajudaram a sanar minhas dúvidas e deixar o ambiente mais leve e divertido (Espero encontrar vocês em uma possível fase 2), e é claro a minha namorada Vitória que sempre me apoia em tudo que eu invento de fazer 💜.