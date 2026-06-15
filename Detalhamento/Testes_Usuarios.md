# Detalhamento dos Testes — `/usuarios`

> Arquivo de referência para os casos de teste implementados em `tests/test_usuarios.py`.
> Endpoint base: `/usuarios`

---

## CT-01 — `test_listar_usuarios`

**Objetivo:** Verificar que o endpoint retorna a lista de usuários cadastrados com o contrato de schema correto.

**Pré-condições:**
- Ao menos um usuário cadastrado (fixture `usuario` garante o POST antes do GET).

**Dados de entrada:** Nenhum (requisição GET sem parâmetros).

**Passos:**
1. Realizar `POST /usuarios` com dados gerados pela fixture `usuario`.
2. Realizar `GET /usuarios`.
3. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O corpo da resposta deve ser válido de acordo com o `SCHEMA_LISTAR_USUARIOS` (campos `quantidade` e `usuarios` presentes).

**Resultado esperado:** Listagem retornada com sucesso e estrutura de dados válida.

---

## CT-02 — `test_cadastrar_usuario_valido`

**Objetivo:** Verificar que um usuário com dados válidos é cadastrado com sucesso e recebe um `_id`.

**Pré-condições:** Nenhuma.

**Dados de entrada:**
- `nome`: nome gerado pelo `faker`.
- `email`: email gerado pelo `faker`.
- `password`: `"teste123"`.
- `administrador`: `"true"`.

**Passos:**
1. Realizar `POST /usuarios` com o payload gerado pela fixture `usuario`.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `201`.
- O campo `message` deve ser `"Cadastro realizado com sucesso"`.
- O campo `_id` deve estar presente no corpo da resposta.

**Resultado esperado:** Usuário cadastrado com sucesso e `_id` retornado.

---

## CT-03 — `test_cadastrar_email_duplicado`

**Objetivo:** Verificar que a API impede o cadastro de dois usuários com o mesmo email.

**Pré-condições:** Nenhuma.

**Dados de entrada:** Mesmo payload enviado duas vezes consecutivas.

**Passos:**
1. Realizar `POST /usuarios` com um payload válido (primeira vez).
2. Realizar `POST /usuarios` com o mesmo payload (segunda vez).
3. Capturar a resposta da segunda requisição.

**Asserções:**
- Status code deve ser `400`.
- O campo `message` deve ser `"Este email já está sendo usado"`.

**Resultado esperado:** API rejeita email duplicado com mensagem de erro clara.

---

## CT-04 — `test_cadastrar_validacao_emoji`

**Objetivo:** Identificar a ausência de validação de formato de email pela API — a qual aceita emojis no endereço.

**Pré-condições:** Nenhuma.

**Dados de entrada:**
- `email`: email com emojis no nome local e domínio (ex.: `"teste123😄😄😄@gmail😄😄.com"`).

**Passos:**
1. Substituir o campo `email` do usuário por uma string com emojis.
2. Realizar `POST /usuarios` com esse payload.
3. Capturar a resposta.

**Asserções:**
- Status code deve ser `201`.
- O campo `message` deve ser `"Cadastro realizado com sucesso"`.

**Resultado esperado:** A API aceita o email com emojis — comportamento identificado como **bug** (severidade Alta). O esperado seria um `400` com mensagem de validação.

> **Defeito registrado:** `POST /usuarios` aceita emojis no corpo e no domínio do email sem validação adequada.

---

## CT-05 — `test_cadastrar_campos_vazios`

**Objetivo:** Verificar que a API valida os campos obrigatórios e rejeita payloads com strings vazias.

**Pré-condições:** Nenhuma.

**Dados de entrada:**
- `nome`: `""`.
- `email`: `""`.
- `password`: `""`.
- `administrador`: `"true"`.

**Passos:**
1. Realizar `POST /usuarios` com todos os campos vazios.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.

**Resultado esperado:** API retorna erro de validação por campos obrigatórios não preenchidos.

---

## CT-06 — `test_buscar_usuario_por_id`

**Objetivo:** Verificar que é possível buscar um usuário existente pelo seu `_id` e que os dados retornados seguem o schema correto.

**Pré-condições:**
- Usuário previamente cadastrado (fixture `usuario_cadastrado`).

**Dados de entrada:**
- `_id` obtido da fixture `usuario_cadastrado`.

**Passos:**
1. Realizar `GET /usuarios/{_id}` com o ID do usuário cadastrado.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O corpo da resposta deve ser válido de acordo com o `SCHEMA_USUARIO`.

**Resultado esperado:** Dados do usuário retornados com sucesso e estrutura válida.

> **Defeito registrado:** O campo `password` é retornado em texto plano na resposta (severidade Crítica).

---

## CT-07 — `test_buscar_usuario_inexistente`

**Objetivo:** Verificar que a API retorna erro ao buscar um usuário com ID inexistente.

**Pré-condições:** Nenhuma.

**Dados de entrada:**
- `_id`: `"0000aaaa1111bbbb"` (ID fixo, garantidamente inexistente).

**Passos:**
1. Realizar `GET /usuarios/0000aaaa1111bbbb`.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.
- O campo `message` deve ser `"Usuário não encontrado"`.

**Resultado esperado:** API retorna erro informativo ao tentar buscar ID inválido.

> **Nota:** A documentação da API não informa que o ID deve ter exatamente 16 caracteres alfanuméricos para retornar `400`. IDs fora desse formato podem resultar em comportamentos distintos.

---

## CT-08 — `test_atualizar_usuario`

**Objetivo:** Verificar que é possível atualizar os dados de um usuário existente.

**Pré-condições:**
- Usuário previamente cadastrado (fixture `usuario_cadastrado`).

**Dados de entrada:**
- `_id` do usuário cadastrado.
- Novo payload gerado por `gerar_usuario()`.

**Passos:**
1. Realizar `PUT /usuarios/{_id}` com um novo payload de dados válidos.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O campo `message` deve ser `"Registro alterado com sucesso"`.

**Resultado esperado:** Dados do usuário atualizados com sucesso.

---

## CT-09 — `test_atualizar_usuario_inexistente`

**Objetivo:** Verificar o comportamento de upsert da API ao tentar atualizar um usuário com ID inexistente.

**Pré-condições:** Nenhuma.

**Dados de entrada:**
- `_id`: `"0000aaaa1111bbbb"` (ID inexistente).
- Payload gerado por `gerar_usuario()`.

**Passos:**
1. Realizar `PUT /usuarios/0000aaaa1111bbbb` com um payload válido.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `201`.
- O campo `message` deve ser `"Cadastro realizado com sucesso"`.
- O campo `_id` deve estar presente e não ser `None`.

**Resultado esperado:** A API cria um novo usuário quando o ID informado não existe (comportamento upsert).

---

## CT-10 — `test_excluir_usuario`

**Objetivo:** Verificar que é possível excluir um usuário existente pelo seu `_id`.

**Pré-condições:**
- Usuário previamente cadastrado (fixture `usuario_cadastrado`).

**Dados de entrada:**
- `_id` do usuário cadastrado.

**Passos:**
1. Realizar `DELETE /usuarios/{_id}`.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.

**Resultado esperado:** Usuário excluído com sucesso.

---

## CT-11 — `test_excluir_usuario_inexistente`

**Objetivo:** Verificar que a API responde com `200` ao tentar excluir um usuário inexistente, com mensagem indicando ausência de registro.

**Pré-condições:** Nenhuma.

**Dados de entrada:**
- `_id`: `"123456"` (ID inexistente).

**Passos:**
1. Realizar `DELETE /usuarios/123456`.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O campo `message` deve ser `"Nenhum registro excluído"`.

**Resultado esperado:** API retorna sucesso sem lançar erro, informando que nenhum registro foi afetado.

---

## CT-12 — `test_excluir_usuario_com_carrinho`

**Objetivo:** Verificar que a API impede a exclusão de um usuário que possui um carrinho ativo.

**Pré-condições:**
- Usuário com perfil de administrador cadastrado e autenticado (fixtures `usuario_cadastrado`, `token`).
- Produto cadastrado (fixture `produto_cadastrado`).

**Dados de entrada:**
- Carrinho criado via `POST /carrinhos` com o produto cadastrado.
- `_id` do usuário cadastrado.

**Passos:**
1. Criar um carrinho para o usuário via `POST /carrinhos`.
2. Tentar excluir o usuário via `DELETE /usuarios/{_id}`.
3. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.
- O campo `message` deve ser `"Não é permitido excluir usuário com carrinho cadastrado"`.

**Resultado esperado:** API bloqueia a exclusão do usuário por regra de integridade referencial.

---

## Notas gerais

- Todos os testes utilizam dados gerados dinamicamente pelo `faker` — sem dados fixos hardcoded, exceto nos cenários negativos com IDs inválidos propositais.
- A fixture `usuario_cadastrado` realiza limpeza automática (DELETE) ao término de cada teste que a utiliza.
- O comportamento de upsert nos endpoints `PUT` é uma característica da API ServeRest, não um bug.