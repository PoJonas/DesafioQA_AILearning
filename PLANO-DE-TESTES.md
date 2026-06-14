# Plano de Testes — DesafioQA AI/R Learning

> **Status:** Em andamento — este documento é atualizado conforme a suíte evolui.

---

## 1. Objetivo

Validar o comportamento da API [ServeRest](https://serverest.dev) nos seus quatro endpoints principais (`/usuarios`, `/login`, `/produtos`, `/carrinhos`), cobrindo fluxos positivos, negativos e regras de negócio críticas, com foco em confiabilidade, segurança e contrato da API.

---

## 2. Estratégia

| Aspecto | Decisão |
|---|---|
| **Tipo de teste** | Testes de API (caixa-preta) |
| **Camada** | Integração — requisições HTTP diretas contra a API |
| **Abordagem** | Funcional + contrato (JSON Schema) |
| **Ferramentas** | Python 3.x, pytest, requests, faker, jsonschema |
| **Ambiente** | CompassUOL ServeRest — `https://compassuol.serverest.dev` |
| **Dados** | Gerados dinamicamente via `faker` a cada execução |
| **Autenticação** | Token JWT obtido via `/login` e reutilizado nas fixtures |

---

## 3. Escopo

### Dentro do escopo

- Todos os endpoints públicos do ServeRest: `/usuarios`, `/login`, `/produtos`, `/carrinhos`
- Fluxos positivos (happy path) de cada operação CRUD
- Fluxos negativos: campos ausentes, dados inválidos, IDs inexistentes
- Regras de negócio: autenticação obrigatória, permissão de administrador, unicidade de email/produto/carrinho
- Validação de contrato via JSON Schema em endpoints selecionados

### Fora do escopo

- Testes de performance e carga
- Testes de segurança avançados (ex: SQL injection, XSS)
- Interface web do ServeRest
- Fluxos que dependem de dados persistentes entre execuções

---

## 4. Cenários a implementar

Todos os testes abaixo estão sujeitos a alterações visto que a suíte ainda não foi finalizada.

### `/usuarios`

| # | Teste | Método | Cenário | Status |
|---|---|---|---|---|
| 01 | `test_listar_usuarios` | GET | Retorna 200 e campo `usuarios` | ✅ Implementado |
| 02 | `test_cadastrar_usuario_valido` | POST | Dados válidos → 201 e `_id` | ✅ Implementado |
| 03 | `test_cadastrar_email_duplicado` | POST | Email já existente → 400 | ✅ Implementado |
| 04 | `test_cadastrar_sem_email` | POST | Body sem `email` → 400 | ✅ Implementado |
| 05 | `test_cadastrar_sem_nome` | POST | Body sem `nome` → 400 | ✅ Implementado |
| 06 | `test_buscar_usuario_por_id` | GET | ID válido → 200 e dados corretos | ✅ Implementado |
| 07 | `test_buscar_usuario_inexistente` | GET | ID inválido → 400 | ✅ Implementado |
| 08 | `test_atualizar_usuario` | PUT | Dados válidos → 200 | ✅ Implementado |
| 09 | `test_excluir_usuario` | DELETE | ID válido → 200 | ✅ Implementado |
| 10 | `test_excluir_usuario_inexistente` | DELETE | ID inexistente → 200 | ✅ Implementado |

### `/login`

| # | Teste | Método | Cenário | Status |
|---|---|---|---|---|
| 11 | `test_login_valido` | POST | Credenciais corretas → 200 + token | ✅ Implementado |
| 12 | `test_login_email_invalido` | POST | Email inexistente → 401 | ✅ Implementado |
| 13 | `test_login_senha_invalida` | POST | Senha incorreta → 401 | ✅ Implementado |
| 14 | `test_login_campos_vazios` | POST | Email e senha vazios → 400 | 🔲 Pendente |

### `/produtos`

| # | Teste | Método | Cenário | Status |
|---|---|---|---|---|
| 15 | `test_listar_produtos` | GET | Retorna 200 e campo `produtos` | 🔲 Pendente |
| 16 | `test_cadastrar_produto_admin` | POST | Token de admin válido → 201 | 🔲 Pendente |
| 17 | `test_cadastrar_produto_sem_token` | POST | Sem token → 401 | 🔲 Pendente |
| 18 | `test_cadastrar_produto_token_nao_admin` | POST | Token de usuário comum → 403 | 🔲 Pendente |
| 19 | `test_cadastrar_produto_nome_duplicado` | POST | Nome já existente → 400 | 🔲 Pendente |
| 20 | `test_cadastrar_produto_campo_ausente` | POST | Body sem `preco` → 400 | 🔲 Pendente |
| 21 | `test_buscar_produto_por_id` | GET | ID válido → 200 e dados corretos | 🔲 Pendente |
| 22 | `test_buscar_produto_inexistente` | GET | ID inválido → 400 | 🔲 Pendente |
| 23 | `test_atualizar_produto_admin` | PUT | Token de admin + dados válidos → 200 | 🔲 Pendente |
| 24 | `test_atualizar_produto_sem_token` | PUT | Sem token → 401 | 🔲 Pendente |
| 25 | `test_excluir_produto_admin` | DELETE | Token de admin → 200 | 🔲 Pendente |
| 26 | `test_excluir_produto_sem_token` | DELETE | Sem token → 401 | 🔲 Pendente |

### `/carrinhos`

| # | Teste | Método | Cenário | Status |
|---|---|---|---|---|
| 27 | `test_listar_carrinhos` | GET | Retorna 200 e campo `carrinhos` | 🔲 Pendente |
| 28 | `test_criar_carrinho_valido` | POST | Token válido + produto existente → 201 | 🔲 Pendente |
| 29 | `test_criar_carrinho_sem_token` | POST | Sem token → 401 | 🔲 Pendente |
| 30 | `test_criar_segundo_carrinho` | POST | Usuário já tem carrinho → 400 | 🔲 Pendente |
| 31 | `test_criar_carrinho_produto_inexistente` | POST | ID de produto inválido → 400 | 🔲 Pendente |
| 32 | `test_fechar_carrinho` | DELETE | `/concluir-compra` com token → 200 | 🔲 Pendente |
| 33 | `test_cancelar_carrinho` | DELETE | `/cancelar-compra` com token → 200 | 🔲 Pendente |

---

## 5. Critérios de qualidade

Um teste é considerado pronto quando:

- [ ] Valida o status code esperado
- [ ] Valida pelo menos um campo do body da resposta
- [ ] É independente — não depende da ordem de execução
- [ ] Usa dados dinâmicos gerados via `faker` (sem dados fixos hardcoded)
- [ ] Tem nome descritivo que indica o cenário testado
- [ ] Passa de forma consistente em pelo menos 3 execuções consecutivas

---

## 6. Bugs identificados

| # | Endpoint | Descrição | Severidade | Issue |
|---|---|---|---|---|

---

## 7. Histórico de atualizações

| Data | Alteração |
|---|---|
| 14/06/2026 | Documento criado com planejamento inicial |