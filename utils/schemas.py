# Schemas JSON para validação de contrato da API ServeRest
# Utilizar com: from jsonschema import validate
# Referência: https://serverest.dev

# --------------------------
# /usuarios

SCHEMA_LISTAR_USUARIOS = {
    "type": "object",
    "required": ["quantidade", "usuarios"],
    "properties": {
        "quantidade": {"type": "integer"},
        "usuarios": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["_id", "nome", "email", "password", "administrador"],
                "properties": {
                    "_id":           {"type": "string"},
                    "nome":          {"type": "string"},
                    "email":         {"type": "string"},
                    "password":      {"type": "string"},
                    "administrador": {"type": "string", "enum": ["true", "false"]}
                }
            }
        }
    }
}

SCHEMA_USUARIO = {
    "type": "object",
    "required": ["_id", "nome", "email", "password", "administrador"],
    "properties": {
        "_id":           {"type": "string"},
        "nome":          {"type": "string"},
        "email":         {"type": "string", "format": "email"},
        "password":      {"type": "string"},
        "administrador": {"type": "string", "enum": ["true", "false"]}
    }
}


# --------------------------
# /login

SCHEMA_LOGIN = {
    "type": "object",
    "required": ["message", "authorization"],
    "properties": {
        "message":       {"type": "string"},
        "authorization": {"type": "string"}
    }
}


# --------------------------
# Schema do endpoint /produtos

SCHEMA_LISTAR_PRODUTOS = {
    "type": "object",
    "required": ["quantidade", "produtos"],
    "properties": {
        "quantidade": {"type": "number"},
        "produtos": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["_id", "nome", "preco", "descricao", "quantidade"],
                "properties": {
                    "_id":       {"type": "string"},
                    "nome":      {"type": "string"},
                    "preco":     {"type": "integer", "minimum": 1},
                    "descricao": {"type": "string"},
                    "quantidade": {"type": "integer", "minimum": 0}
                }
            }
        }
    }
}

SCHEMA_PRODUTO = {
    "type": "object",
    "required": ["_id", "nome", "preco", "descricao", "quantidade"],
    "properties": {
        "_id":        {"type": "string"},
        "nome":       {"type": "string"},
        "preco":      {"type": "integer", "minimum": 1},
        "descricao":  {"type": "string"},
        "quantidade": {"type": "integer", "minimum": 0}
    }
}

# --------------------------
# /carrinhos

SCHEMA_LISTAR_CARRINHOS = {
    "type": "object",
    "required": ["quantidade", "carrinhos"],
    "properties": {
        "quantidade": {"type": "number"},
        "carrinhos": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["_id", "produtos", "precoTotal", "quantidadeTotal", "idUsuario"],
                "properties": {
                    "_id":             {"type": "string"},
                    "precoTotal":      {"type": "integer", "minimum": 0},
                    "quantidadeTotal": {"type": "integer", "minimum": 0},
                    "idUsuario":       {"type": "string"},
                    "produtos": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["idProduto", "quantidade", "precoUnitario"],
                            "properties": {
                                "idProduto":     {"type": "string"},
                                "quantidade":    {"type": "integer", "minimum": 1},
                                "precoUnitario": {"type": "integer", "minimum": 0}
                            }
                        }
                    }
                }
            }
        }
    }
}

SCHEMA_CARRINHO = {
    "type": "object",
    "required": ["_id", "produtos", "precoTotal", "quantidadeTotal", "idUsuario"],
    "properties": {
        "_id":             {"type": "string"},
        "precoTotal":      {"type": "integer", "minimum": 0},
        "quantidadeTotal": {"type": "integer", "minimum": 0},
        "idUsuario":       {"type": "string"},
        "produtos": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["idProduto", "quantidade", "precoUnitario"],
                "properties": {
                    "idProduto":     {"type": "string"},
                    "quantidade":    {"type": "integer", "minimum": 1},
                    "precoUnitario": {"type": "integer", "minimum": 0}
                }
            }
        }
    }
}
