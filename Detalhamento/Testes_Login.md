# Detalhamento dos Testes — `/login`

> Arquivo de referência para os casos de teste implementados em `tests/test_login.py`.
> Endpoint base: `POST /login`

---

## CT-13 — `test_login_valido`

**Objetivo:** Verificar que um usuário com credenciais válidas consegue autenticar-se com sucesso e recebe um token de autorização.

**Pré-condições:**
- Usuário previamente cadastrado na API (fixture `usuario_cadastrado`).

**Dados de entrada:**
- `email`: email gerado dinamicamente pelo `faker` e cadastrado na fixture.
- `password`: `"teste123"` (valor fixo definido em `gerar_usuario()`).

**Passos:**
1. Realizar `POST /login` com `email` e `password` do usuário cadastrado.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `200`.
- O corpo da resposta deve ser válido de acordo com o `SCHEMA_LOGIN` (campos `message` e `authorization` presentes e do tipo `string`).

**Resultado esperado:** Login realizado com sucesso, token JWT retornado no campo `authorization`.

---

## CT-14 — `test_login_email_invalido`

**Objetivo:** Garantir que a API rejeita tentativas de login com um email não cadastrado.

**Pré-condições:**
- Usuário cadastrado (fixture `usuario_cadastrado`) para utilizar uma senha válida.

**Dados de entrada:**
- `email`: `"naoexiste@email.com"` (email fixo, garantidamente não cadastrado).
- `password`: senha válida do usuário cadastrado.

**Passos:**
1. Realizar `POST /login` com o email inexistente e a senha correta.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `401`.
- O campo `message` do corpo da resposta deve ser igual a `"Email e/ou senha inválidos"`.

**Resultado esperado:** Autenticação negada por email não encontrado na base.

---

## CT-15 — `test_login_senha_invalida`

**Objetivo:** Garantir que a API rejeita tentativas de login com senha incorreta para um email válido.

**Pré-condições:**
- Usuário cadastrado (fixture `usuario_cadastrado`).

**Dados de entrada:**
- `email`: email válido do usuário cadastrado.
- `password`: `"senha_errada"` (valor incorreto).

**Passos:**
1. Realizar `POST /login` com o email correto e a senha incorreta.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `401`.
- O campo `message` do corpo da resposta deve ser igual a `"Email e/ou senha inválidos"`.

**Resultado esperado:** Autenticação negada por credencial incorreta.

---

## CT-16 — `test_login_campos_vazios`

**Objetivo:** Garantir que a API valida os campos obrigatórios e rejeita requisições com `email` e `password` vazios.

**Pré-condições:** Nenhuma (não requer usuário cadastrado).

**Dados de entrada:**
- `email`: `""` (string vazia).
- `password`: `""` (string vazia).

**Passos:**
1. Realizar `POST /login` com ambos os campos vazios.
2. Capturar a resposta.

**Asserções:**
- Status code deve ser `400`.

**Resultado esperado:** API retorna erro de validação por campos obrigatórios não preenchidos.

---

## Notas gerais

- Todos os testes desta suíte são independentes entre si.
- A fixture `usuario_cadastrado` garante criação e limpeza automática do usuário de teste.
- A mensagem de erro `"Email e/ou senha inválidos"` é deliberadamente genérica pela API para não revelar qual dos dois campos está errado, o que é uma boa prática de segurança.