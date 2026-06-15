# Detalhamento dos Testes — `/produtos`

> Arquivo de referência para os casos de teste implementados em `tests/test_produtos.py`.
> Endpoint base: `/produtos`

---

## CT-17 — `test_listar_produtos`

**Objetivo:** Verificar que o endpoint retorna a listagem de produtos com o contrato de schema correto.

**Pré-condições:** Nenhuma.

**Dados de entrada:** Nenhum (requisição GET sem parâmetros).

**Passos:**
1. Realizar `GET /produtos`.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O corpo da resposta deve ser válido de acordo com o `SCHEMA_LISTAR_PRODUTOS` (campos `quantidade` e `produtos` presentes).

**Resultado esperado:** Listagem de produtos retornada com sucesso e estrutura de dados válida.

---

## CT-18 — `test_cadastrar_produto_valido`

**Objetivo:** Verificar que um produto com dados válidos pode ser cadastrado por um administrador autenticado.

**Pré-condições:**
- Usuário administrador cadastrado e token obtido (fixture `token`).

**Dados de entrada:**
- Payload gerado por `gerar_produto()`: `nome`, `preco`, `descricao`, `quantidade`.
- Header `Authorization` com token de administrador.

**Passos:**
1. Realizar `POST /produtos` com payload válido e token de admin no header.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `201`.
- O campo `_id` deve estar presente no corpo da resposta.

**Resultado esperado:** Produto cadastrado com sucesso e `_id` retornado.

---

## CT-19 — `test_cadastrar_produto_sem_token`

**Objetivo:** Verificar que a API rejeita o cadastro de produto sem token de autenticação.

**Pré-condições:** Nenhuma.

**Dados de entrada:**
- Payload gerado por `gerar_produto()`.
- Sem header `Authorization`.

**Passos:**
1. Realizar `POST /produtos` sem o header de autorização.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `401`.
- O campo `message` deve ser `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"`.

**Resultado esperado:** API rejeita a requisição por ausência de autenticação.

---

## CT-20 — `test_cadastrar_produto_token_nao_admin`

**Objetivo:** Verificar que a API rejeita o cadastro de produto por um usuário sem perfil de administrador.

**Pré-condições:**
- Usuário não-administrador cadastrado e token obtido (fixture `token_nao_admin`).

**Dados de entrada:**
- Payload gerado por `gerar_produto()`.
- Header `Authorization` com token de usuário comum.

**Passos:**
1. Realizar `POST /produtos` com token de usuário não-admin.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `403`.
- O campo `message` deve ser `"Rota exclusiva para administradores"`.

**Resultado esperado:** API rejeita a requisição por falta de permissão.

---

## CT-21 — `test_cadastrar_produto_nome_duplicado`

**Objetivo:** Verificar que a API impede o cadastro de dois produtos com o mesmo nome.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Novo payload gerado por `gerar_produto()` com `nome` substituído pelo nome do produto já cadastrado.

**Passos:**
1. Gerar um novo payload e sobrescrever o `nome` com o nome do produto cadastrado.
2. Realizar `POST /produtos` com esse payload e token de admin.
3. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.
- O campo `message` deve ser `"Já existe produto com esse nome"`.

**Resultado esperado:** API rejeita nome duplicado com mensagem de erro clara.

---

## CT-22 — `test_cadastrar_produto_campo_ausente`

**Objetivo:** Verificar que a API valida campos obrigatórios e rejeita payloads incompletos.

**Pré-condições:**
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Payload gerado por `gerar_produto()` com o campo `preco` removido.

**Passos:**
1. Gerar um payload válido e deletar a chave `preco`.
2. Realizar `POST /produtos` com o payload incompleto e token de admin.
3. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.
- O campo `preco` deve estar presente no corpo da resposta de erro (indicando qual campo falhou na validação).

**Resultado esperado:** API retorna erro de validação indicando o campo ausente.

---

## CT-23 — `test_cadastrar_produto_preco_invalido`

**Objetivo:** Verificar que a API rejeita preços negativos no cadastro de produtos.

**Pré-condições:**
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Payload gerado por `gerar_produto()` com `preco` substituído por `-1`.

**Passos:**
1. Gerar um payload válido e sobrescrever `preco` com `-1`.
2. Realizar `POST /produtos` com esse payload e token de admin.
3. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.

**Resultado esperado:** API rejeita preço negativo por violação de regra de validação.

> **Defeito registrado:** A API aceita valores extremamente altos no campo `preco` sem validação de limite superior, podendo causar overflow do tipo integer (severidade Média).

---

## CT-24 — `test_buscar_produto_por_id`

**Objetivo:** Verificar que é possível buscar um produto existente pelo seu `_id` e que os dados retornados seguem o schema correto.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).

**Dados de entrada:**
- `_id` do produto cadastrado.

**Passos:**
1. Realizar `GET /produtos/{_id}` com o ID do produto.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O corpo da resposta deve ser válido de acordo com o `SCHEMA_PRODUTO`.

**Resultado esperado:** Dados do produto retornados com sucesso e estrutura válida.

---

## CT-25 — `test_buscar_produto_inexistente`

**Objetivo:** Verificar que a API retorna erro ao buscar um produto com ID inexistente.

**Pré-condições:** Nenhuma.

**Dados de entrada:**
- `_id`: `"0000aaaa1111bbbb"` (ID fixo, garantidamente inexistente).

**Passos:**
1. Realizar `GET /produtos/0000aaaa1111bbbb`.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.
- O campo `message` deve ser `"Produto não encontrado"`.

**Resultado esperado:** API retorna erro informativo ao tentar buscar ID inválido.

---

## CT-26 — `test_atualizar_produto`

**Objetivo:** Verificar que um administrador autenticado pode atualizar os dados de um produto existente.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de administrador (fixture `token`).

**Dados de entrada:**
- `_id` do produto cadastrado.
- Novo payload gerado por `gerar_produto()`.

**Passos:**
1. Realizar `PUT /produtos/{_id}` com novo payload e token de admin.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O campo `message` deve ser `"Registro alterado com sucesso"`.

**Resultado esperado:** Produto atualizado com sucesso.

---

## CT-27 — `test_atualizar_produto_sem_token`

**Objetivo:** Verificar que a API rejeita a atualização de produto sem token de autenticação.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).

**Dados de entrada:**
- `_id` do produto cadastrado.
- Novo payload gerado por `gerar_produto()`.
- Sem header `Authorization`.

**Passos:**
1. Realizar `PUT /produtos/{_id}` sem o header de autorização.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `401`.
- O campo `message` deve ser `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"`.

**Resultado esperado:** API rejeita a requisição por ausência de autenticação.

---

## CT-28 — `test_atualizar_produto_token_nao_admin`

**Objetivo:** Verificar que a API rejeita a atualização de produto por um usuário sem perfil de administrador.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de usuário não-admin (fixture `token_nao_admin`).

**Dados de entrada:**
- `_id` do produto cadastrado.
- Novo payload gerado por `gerar_produto()`.
- Header `Authorization` com token de usuário comum.

**Passos:**
1. Realizar `PUT /produtos/{_id}` com token de não-admin.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `403`.
- O campo `message` deve ser `"Rota exclusiva para administradores"`.

**Resultado esperado:** API rejeita a requisição por falta de permissão.

---

## CT-29 — `test_atualizar_produto_inexistente`

**Objetivo:** Verificar o comportamento de upsert da API ao tentar atualizar um produto com ID inexistente.

**Pré-condições:**
- Token de administrador (fixture `token`).

**Dados de entrada:**
- `_id`: `"0000aaaa1111bbbb"` (ID inexistente).
- Payload gerado por `gerar_produto()`.

**Passos:**
1. Realizar `PUT /produtos/0000aaaa1111bbbb` com payload válido e token de admin.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `201`.
- O campo `message` deve ser `"Cadastro realizado com sucesso"`.
- O campo `_id` deve ser diferente de `None`.

**Resultado esperado:** A API cria um novo produto quando o ID informado não existe (comportamento upsert).

---

## CT-30 — `test_atualizar_produto_nome_duplicado`

**Objetivo:** Verificar que a API impede a atualização do nome de um produto para um nome que já existe em outro produto.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Um segundo produto criado durante o teste.
- Payload de atualização com `nome` igual ao do primeiro produto.

**Passos:**
1. Criar um segundo produto via `POST /produtos` com token de admin.
2. Tentar atualizar o segundo produto com o nome do primeiro via `PUT /produtos/{segundo_id}`.
3. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.
- O campo `message` deve ser `"Já existe produto com esse nome"`.

**Resultado esperado:** API rejeita nome duplicado na atualização.

---

## CT-31 — `test_excluir_produto`

**Objetivo:** Verificar que um administrador autenticado pode excluir um produto existente.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de administrador (fixture `token`).

**Dados de entrada:**
- `_id` do produto cadastrado.

**Passos:**
1. Realizar `DELETE /produtos/{_id}` com token de admin.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O campo `message` deve ser `"Registro excluído com sucesso"`.

**Resultado esperado:** Produto excluído com sucesso.

---

## CT-32 — `test_excluir_produto_sem_token`

**Objetivo:** Verificar que a API rejeita a exclusão de produto sem token de autenticação.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).

**Dados de entrada:**
- `_id` do produto cadastrado.
- Sem header `Authorization`.

**Passos:**
1. Realizar `DELETE /produtos/{_id}` sem o header de autorização.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `401`.
- O campo `message` deve ser `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"`.

**Resultado esperado:** API rejeita a requisição por ausência de autenticação.

---

## CT-33 — `test_excluir_produto_token_nao_admin`

**Objetivo:** Verificar que a API rejeita a exclusão de produto por usuário sem perfil de administrador.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de usuário não-admin (fixture `token_nao_admin`).

**Dados de entrada:**
- `_id` do produto cadastrado.
- Header `Authorization` com token de usuário comum.

**Passos:**
1. Realizar `DELETE /produtos/{_id}` com token de não-admin.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `403`.
- O campo `message` deve ser `"Rota exclusiva para administradores"`.

**Resultado esperado:** API rejeita a requisição por falta de permissão.

---

## CT-34 — `test_excluir_produto_no_carrinho`

**Objetivo:** Verificar que a API impede a exclusão de um produto que está associado a algum carrinho ativo.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Carrinho criado via `POST /carrinhos` com o produto cadastrado.
- `_id` do produto cadastrado.

**Passos:**
1. Criar um carrinho associando o produto via `POST /carrinhos` com token de admin.
2. Tentar excluir o produto via `DELETE /produtos/{_id}` com token de admin.
3. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.
- O campo `message` deve conter a palavra `"carrinho"` (verificado via `.lower()`).

**Resultado esperado:** API bloqueia a exclusão do produto por regra de integridade referencial.

---

## Notas gerais

- Todas as operações de escrita (`POST`, `PUT`, `DELETE`) requerem token de administrador.
- A fixture `produto_cadastrado` não realiza cleanup automático após o teste — o produto pode precisar ser removido manualmente se o teste falhar antes da limpeza.
- O comportamento de upsert em `PUT /produtos/{_id}` é intencional na API ServeRest.
- Nomes de produtos são gerados com `fake.unique.bothify()` para evitar colisões entre execuções paralelas.