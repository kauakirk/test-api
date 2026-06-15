import uuid


def new_user_payload(administrador="false"):
    unique_id = uuid.uuid4().hex
    return {
        "nome": f"User {unique_id}",
        "email": f"user_{unique_id}@qa.com",
        "password": "teste123",
        "administrador": administrador,
    }


def new_product_payload():
    unique_id = uuid.uuid4().hex
    return {
        "nome": f"Produto Teste {unique_id}",
        "preco": 100,
        "descricao": "Produto de teste",
        "quantidade": 10,
    }
