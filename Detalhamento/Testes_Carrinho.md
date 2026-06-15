# Detalhamento dos Testes — `/carrinhos`

> Arquivo de referência para os casos de teste implementados em `tests/test_carrinhos.py`.
> Endpoints cobertos: `GET /carrinhos`, `POST /carrinhos`, `DELETE /carrinhos/concluir-compra`, `DELETE /carrinhos/cancelar-compra`

---

## CT-35 — `test_listar_carrinhos`

**Objetivo:** Verificar que o endpoint retorna a listagem de carrinhos com o contrato de schema correto.

**Pré-condições:** Nenhuma.

**Dados de entrada:** Nenhum (requisição GET sem parâmetros).

**Passos:**
1. Realizar `GET /carrinhos`.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O corpo da resposta deve ser válido de acordo com o `SCHEMA_LISTAR_CARRINHOS` (campos `quantidade` e `carrinhos` presentes).

**Resultado esperado:** Listagem de carrinhos retornada com sucesso e estrutura de dados válida.

---

## CT-36 — `test_listar_carrinhos_com_parametros_errados`

**Objetivo:** Verificar que a API rejeita parâmetros de query com valores inválidos.

**Pré-condições:** Nenhuma.

**Dados de entrada:**
- Query param `quantidade` com valor `-1`.

**Passos:**
1. Realizar `GET /carrinhos?quantidade=-1`.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.

**Resultado esperado:** API retorna erro de validação ao receber parâmetros negativos ou inválidos.

---

## CT-37 — `test_criar_carrinho_valido`

**Objetivo:** Verificar que um carrinho criado com dados válidos pode ser recuperado com sucesso.

**Pré-condições:**
- Carrinho previamente criado (fixture `carrinho_cadastrado`).

**Dados de entrada:**
- `_id` do carrinho cadastrado pela fixture.

**Passos:**
1. Realizar `GET /carrinhos/{_id}` com o ID do carrinho criado pela fixture.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O corpo da resposta deve ser válido de acordo com o `SCHEMA_CARRINHO`.

**Resultado esperado:** Carrinho criado e recuperado com sucesso, estrutura de dados válida.

---

## CT-38 — `test_criar_carrinho_sem_token`

**Objetivo:** Verificar que a API rejeita a criação de carrinho sem token de autenticação.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).

**Dados de entrada:**
- Payload com o `_id` do produto cadastrado e `quantidade: 1`.
- Sem header `Authorization`.

**Passos:**
1. Realizar `POST /carrinhos` sem o header de autorização.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `401`.
- O campo `message` deve ser `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"`.

**Resultado esperado:** API rejeita a requisição por ausência de autenticação.

---

## CT-39 — `test_criar_carrinho_token_nao_admin`

**Objetivo:** Verificar que usuários sem perfil de administrador também podem criar carrinhos.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de usuário não-admin (fixture `token_nao_admin`).

**Dados de entrada:**
- Payload com o `_id` do produto e `quantidade: 1`.
- Header `Authorization` com token de usuário comum.

**Passos:**
1. Realizar `POST /carrinhos` com token de não-admin.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `201`.
- O campo `_id` deve estar presente no corpo da resposta.

**Resultado esperado:** Carrinho criado com sucesso — a criação de carrinho não exige perfil de administrador.

---

## CT-40 — `test_criar_segundo_carrinho`

**Objetivo:** Verificar que a API impede que um mesmo usuário tenha mais de um carrinho ativo simultaneamente.

**Pré-condições:**
- Carrinho previamente criado para o usuário admin (fixture `carrinho_cadastrado`).
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Payload com o produto já existente no carrinho e `quantidade: 1`.

**Passos:**
1. Tentar criar um segundo carrinho via `POST /carrinhos` para o mesmo usuário.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.
- O campo `message` deve ser `"Não é permitido ter mais de 1 carrinho"`.

**Resultado esperado:** API bloqueia a criação de carrinho duplicado por regra de negócio.

---

## CT-41 — `test_criar_carrinho_com_produto_duplicado`

**Objetivo:** Verificar que a API rejeita carrinhos com o mesmo produto listado mais de uma vez.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Payload com o mesmo `idProduto` duplicado no array `produtos`, com quantidades diferentes (`1` e `2`).

**Passos:**
1. Realizar `POST /carrinhos` com o mesmo produto duas vezes no array.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.
- O campo `message` deve ser `"Não é permitido possuir produto duplicado"`.

**Resultado esperado:** API rejeita a duplicação de produto no carrinho.

---

## CT-42 — `test_criar_carrinho_produto_inexistente`

**Objetivo:** Verificar que a API rejeita a criação de carrinho com um produto cujo ID não existe.

**Pré-condições:**
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Payload com `idProduto: "0000aaaa1111bbbb"` (ID inexistente) e `quantidade: 1`.

**Passos:**
1. Realizar `POST /carrinhos` com um ID de produto inválido.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.
- O campo `message` deve ser `"Produto não encontrado"`.

**Resultado esperado:** API rejeita carrinho com referência a produto inexistente.

---

## CT-43 — `test_criar_carrinho_produto_qtd_invalida`

**Objetivo:** Verificar que a API rejeita carrinhos com quantidade de produto igual a zero.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Payload com `idProduto` válido e `quantidade: 0`.

**Passos:**
1. Realizar `POST /carrinhos` com quantidade `0` no produto.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.

**Resultado esperado:** API rejeita quantidade inválida (zero não é permitido).

---

## CT-44 — `test_buscar_carrinho_por_id`

**Objetivo:** Verificar que é possível recuperar um carrinho existente pelo seu `_id`.

**Pré-condições:**
- Carrinho previamente criado (fixture `carrinho_cadastrado`).

**Dados de entrada:**
- `_id` do carrinho cadastrado.

**Passos:**
1. Realizar `GET /carrinhos/{_id}` com o ID do carrinho.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O corpo da resposta deve ser válido de acordo com o `SCHEMA_CARRINHO`.

**Resultado esperado:** Dados do carrinho retornados com sucesso e estrutura válida.

---

## CT-45 — `test_buscar_carrinho_id_inexistente`

**Objetivo:** Verificar que a API retorna erro ao buscar um carrinho com ID inexistente.

**Pré-condições:** Nenhuma.

**Dados de entrada:**
- `_id`: `"0000aaaa1111bbbb"` (ID fixo, garantidamente inexistente).

**Passos:**
1. Realizar `GET /carrinhos/0000aaaa1111bbbb`.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.
- O campo `message` deve ser `"Carrinho não encontrado"`.

**Resultado esperado:** API retorna erro informativo ao tentar buscar carrinho inexistente.

---

## CT-46 — `test_fechar_carrinho`

**Objetivo:** Verificar que um administrador pode concluir a compra, removendo o carrinho com sucesso.

**Pré-condições:**
- Carrinho previamente criado para o usuário admin (fixture `carrinho_cadastrado`).
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Header `Authorization` com token de admin.

**Passos:**
1. Realizar `DELETE /carrinhos/concluir-compra` com token de admin.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O campo `message` deve ser `"Registro excluído com sucesso"`.

**Resultado esperado:** Compra concluída com sucesso, carrinho removido da base.

---

## CT-47 — `test_fechar_carrinho_token_nao_admin`

**Objetivo:** Verificar que usuários não-administradores também podem concluir a compra de seus próprios carrinhos.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de usuário não-admin (fixture `token_nao_admin`).

**Dados de entrada:**
- Carrinho criado via `POST /carrinhos` com token de não-admin.
- Header `Authorization` com token de não-admin.

**Passos:**
1. Criar um carrinho para o usuário não-admin via `POST /carrinhos`.
2. Realizar `DELETE /carrinhos/concluir-compra` com token de não-admin.
3. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O campo `message` deve ser `"Registro excluído com sucesso"`.

**Resultado esperado:** Compra concluída com sucesso — qualquer usuário autenticado pode concluir sua própria compra.

---

## CT-48 — `test_fechar_carrinho_usuario_sem_carrinho`

**Objetivo:** Verificar que a API responde adequadamente ao tentar concluir compra sem carrinho ativo.

**Pré-condições:**
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Header `Authorization` com token de admin.
- (Carrinho cancelado previamente via `DELETE /carrinhos/cancelar-compra` antes do teste.)

**Passos:**
1. Cancelar o carrinho via `DELETE /carrinhos/cancelar-compra` (para garantir que não existe carrinho).
2. Realizar `DELETE /carrinhos/concluir-compra` sem carrinho ativo.
3. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O campo `message` deve ser `"Não foi encontrado carrinho para esse usuário"`.

**Resultado esperado:** API retorna `200` com mensagem informativa, sem lançar erro 4xx.

---

## CT-49 — `test_cancelar_compra`

**Objetivo:** Verificar que um administrador pode cancelar a compra, removendo o carrinho e reabastecendo o estoque dos produtos.

**Pré-condições:**
- Carrinho previamente criado para o usuário admin (fixture `carrinho_cadastrado`).
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Header `Authorization` com token de admin.

**Passos:**
1. Realizar `DELETE /carrinhos/cancelar-compra` com token de admin.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O campo `message` deve ser `"Registro excluído com sucesso. Estoque dos produtos reabastecido"`.

**Resultado esperado:** Compra cancelada, carrinho removido e estoque dos produtos restaurado.

---

## CT-50 — `test_cancelar_compra_token_nao_admin`

**Objetivo:** Verificar que usuários não-administradores também podem cancelar a compra de seus próprios carrinhos.

**Pré-condições:**
- Produto previamente cadastrado (fixture `produto_cadastrado`).
- Token de usuário não-admin (fixture `token_nao_admin`).

**Dados de entrada:**
- Carrinho criado via `POST /carrinhos` com token de não-admin.
- Header `Authorization` com token de não-admin.

**Passos:**
1. Criar um carrinho para o usuário não-admin via `POST /carrinhos`.
2. Realizar `DELETE /carrinhos/cancelar-compra` com token de não-admin.
3. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O campo `message` deve ser `"Registro excluído com sucesso. Estoque dos produtos reabastecido"`.

**Resultado esperado:** Compra cancelada com sucesso — qualquer usuário autenticado pode cancelar sua própria compra.

---

## CT-51 — `test_cancelar_compra_usuario_sem_carrinho`

**Objetivo:** Verificar que a API responde adequadamente ao tentar cancelar compra sem carrinho ativo.

**Pré-condições:**
- Token de administrador (fixture `token`).

**Dados de entrada:**
- Header `Authorization` com token de admin.
- (Primeiro cancelamento executado antes para garantir estado sem carrinho.)

**Passos:**
1. Realizar `DELETE /carrinhos/cancelar-compra` uma primeira vez (para limpar o estado).
2. Realizar `DELETE /carrinhos/cancelar-compra` novamente, sem carrinho ativo.
3. Capturar a resposta da segunda chamada.

**Asserções:**
- Status code deve ser `200`.
- O campo `message` deve ser `"Não foi encontrado carrinho para esse usuário"`.

**Resultado esperado:** API retorna `200` com mensagem informativa, comportamento idempotente.

---

## Notas gerais

- A criação de carrinho **não** é exclusiva de administradores — qualquer usuário autenticado pode criar e gerenciar seu carrinho.
- A regra de negócio limita **um carrinho por usuário** — tentativas de criar um segundo carrinho são rejeitadas com `400`.
- Os endpoints `/concluir-compra` e `/cancelar-compra` diferem na lógica de estoque: `concluir-compra` não reabastece o estoque; `cancelar-compra` sim.
- A fixture `carrinho_cadastrado` realiza cleanup automático via `DELETE /carrinhos/cancelar-compra` ao término de cada teste.
- Todos os testes são independentes entre si e não dependem de ordem de execução.