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
|---|---|---|---|---|---|
| 01 | `test_listar_usuarios` | GET | Retorna 200 e campo `usuarios` | ✅ Implementado |
| 02 | `test_cadastrar_usuario_valido` | POST | Dados válidos → 201 e `_id` | ✅ Implementado |
| 03 | `test_cadastrar_email_duplicado` | POST | Email já existente → 400 | ✅ Implementado |
| 04 | `test_cadastrar_validacao_emoji` | POST | Não aceita → 400 | ✅ Implementado |
| 05 | `test_cadastrar_campos_vazios` | POST | `Body` vazio → 400 | ✅ Implementado |
| 06 | `test_buscar_usuario_por_id` | GET | ID válido → 200 e dados corretos | ✅ Implementado |
| 07 | `test_buscar_usuario_inexistente` | GET | ID inválido → 400 | ✅ Implementado |
| 08 | `test_atualizar_usuario` | PUT | Dados válidos → 200 | ✅ Implementado |
| 09 | `test_atualizar_usuario_inexistente` | PUT | Dados inexistentes → 201 | ✅ Implementado |
| 10 | `test_excluir_usuario` | DELETE | ID válido → 200 | ✅ Implementado |
| 11 | `test_excluir_usuario_inexistente` | DELETE | ID inexistente → 200 com `message` diferente | ✅ Implementado |
| 12 | `test_excluir_usuario_com_carrinho` | DELETE | Usuário com carrinho ativo → 400 | ✅ Implementado |

### `/login`

| # | Teste | Método | Cenário | Status |
|---|---|---|---|---|---|
| 13 | `test_login_valido` | POST | Credenciais corretas → 200 + token | ✅ Implementado |
| 14 | `test_login_email_invalido` | POST | Email inexistente → 401 | ✅ Implementado |
| 15 | `test_login_senha_invalida` | POST | Senha incorreta → 401 | ✅ Implementado |
| 16 | `test_login_campos_vazios` | POST | Email e senha vazios → 400 | ✅ Implementado |

### `/produtos`

| # | Teste | Método | Cenário | Status |
|---|---|---|---|---|---|
| 17 | `test_listar_produtos` | GET | Retorna 200 e campo `produtos` | ✅ Implementado |
| 18 | `test_cadastrar_produto_valido` | POST | Token de admin válido → 201 | ✅ Implementado |
| 19 | `test_cadastrar_produto_sem_token` | POST | Sem token → 401 | ✅ Implementado |
| 20 | `test_cadastrar_produto_token_nao_admin` | POST | Token de usuário comum → 403 | ✅ Implementado |
| 21 | `test_cadastrar_produto_nome_duplicado` | POST | Nome já existente → 400 | ✅ Implementado |
| 22 | `test_cadastrar_produto_campo_ausente` | POST | Body sem `preco` → 400 | ✅ Implementado |
| 23 | `test_cadastrar_produto_preco_invalido` | POST | Preço negativo → 400 | ✅ Implementado |
| 24 | `test_buscar_produto_por_id` | GET | ID válido → 200 e dados corretos | ✅ Implementado |
| 25 | `test_buscar_produto_inexistente` | GET | ID inválido → 400 | ✅ Implementado |
| 26 | `test_atualizar_produto` | PUT | Token de admin + dados válidos → 200 | ✅ Implementado |
| 27 | `test_atualizar_produto_sem_token` | PUT | Sem token → 401 | ✅ Implementado |
| 28 | `test_atualizar_produto_token_nao_admin` | PUT | Token de usuário comum → 403 | ✅ Implementado |
| 29 | `test_atualizar_produto_inexistente` | PUT | Produto não existe então cria-se um novo → 201 | ✅ Implementado |
| 30 | `test_atualizar_produto_nome_duplicado` | PUT | Atualizar o nome para um já existente → 400 | ✅ Implementado |
| 31 | `test_excluir_produto` | DELETE | Token de admin → 200 | ✅ Implementado |
| 32 | `test_excluir_produto_sem_token` | DELETE | Sem token → 401 | ✅ Implementado |
| 33 | `test_excluir_produto_token_nao_admin` | DELETE | Token de usuário comum → 403 | ✅ Implementado |
| 34 | `test_excluir_produto_no_carrinho` | DELETE | Token de admin → 200 | ✅ Implementado |


### `/carrinhos`

| # | Teste | Método | Cenário | Status |
|---|---|---|---|---|---|
| 35 | `test_listar_carrinhos` | GET | Retorna 200 e campo `carrinhos` | ✅ Implementado |
| 36 | `test_listar_carrinhos_com_parametros_errados` | GET | Parametros negativos ou inexistentes → 400  | ✅ Implementado |
| 37 | `test_criar_carrinho_valido` | POST | Token válido + produto existente → 201 | ✅ Implementado |
| 38 | `test_criar_carrinho_sem_token` | POST | Sem token → 401 | ✅ Implementado |
| 39 | `test_criar_carrinho_token_nao_admin` | POST | Token comum → 403 | ✅ Implementado |
| 40 | `test_criar_segundo_carrinho` | POST | Usuário já tem carrinho → 400 | ✅ Implementado |
| 41 | `test_criar_carrinho_com_produto_duplicado` | POST | Carrinho possui produto duplicado → 400 | ✅ Implementado |
| 42 | `test_criar_carrinho_produto_inexistente` | POST | ID de produto inválido → 400 | ✅ Implementado |
| 43 | `test_criar_carrinho_produto_qtd_invalida` | POST | Produto com quantidade inválida → 400 | ✅ Implementado |
| 44 | `test_buscar_carrinho_por_id` | GET | Procurar um carrinho com ID válido → 200 | ✅ Implementado |
| 45 | `test_buscar_carrinho_id_inexistente` | GET | Procurar um carrinho com ID inexistente → 400 | ✅ Implementado |
| 46 | `test_fechar_carrinho` | DELETE | `/concluir-compra` correto e com token admin → 200 | ✅ Implementado |
| 47 | `test_fechar_carrinho_token_nao_admin` | DELETE | `/concluir-compra` correto mas com token comum → 200 | ✅ Implementado |
| 48 | `test_fechar_carrinho_usuario_sem_carrinho` | DELETE | Concluir a compra sem carrinho ativo → 200 e message de erro | ✅ Implementado |
| 49 | `test_cancelar_compra` | DELETE | `/cancelar-compra` correto e com token admin → 200 | ✅ Implementado |
| 50 | `test_cancelar_compra_token_nao_admin` | DELETE | `/cancelar-compra` correto mas com token comum → 200 | ✅ Implementado |
| 51 | `test_cancelar_compra_usuario_sem_carrinho` | DELETE | Cancelar a compra sem carrinho ativo → 200 e message de erro | ✅ Implementado |

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

## Bugs e lacunas nas regras de negócio identificados

Os bugs e lacunas nas regras de negócio encontrados durante a execução foram reportados como issues no repositório. Abaixo um resumo:

| # | Endpoint | Descrição | Severidade |
|---|---|---|---|
| 1 | `GET /usuarios` | Retorna senha dos usuários em texto plano | Crítica |
| 2 | `POST /usuarios` | Aceita emojis no corpo e domínio do email sem validação | Alta |
| 3 | `GET /usuarios/{_id}` | Retorna senha do usuário em texto plano | Crítica |
| 4 | `GET /usuarios/{_id}` | A documentação não menciona que o ID precisa ter exatamente 16 caracteres alfanuméricos | Baixa |
| 5 | `POST /produtos` | Pode ser colocado qualquer valor no campo de `preco`, podendo estourar o limite do tipo integer | Média |

---

## 7. Histórico de atualizações

| Data | Alteração |
|---|---|
| 14/06/2026 | Documento criado com planejamento inicial |
| 15/06/2026 | Definição de todos os testes que serão implementados |
| 15/06/2026 | Finalização da suíte de testes |
