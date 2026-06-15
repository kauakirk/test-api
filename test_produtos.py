import requests
import uuid

BASE_URL = "https://compassuol.serverest.dev"


def new_user_payload(administrador="false"):
    unique_id = uuid.uuid4().hex
    return {
        "nome": f"Produto User {unique_id}",
        "email": f"produto_user_{unique_id}@qa.com",
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


def create_user(payload):
    return requests.post(BASE_URL + "/usuarios", json=payload)


def do_login(payload):
    return requests.post(BASE_URL + "/login", json=payload)


def create_product(token, payload):
    return requests.post(BASE_URL + "/produtos", json=payload, headers={"Authorization": token})


def create_admin_token():
    admin_payload = new_user_payload(administrador="true")
    create_response = create_user(admin_payload)
    assert create_response.status_code == 201

    login_response = do_login({"email": admin_payload["email"], "password": admin_payload["password"]})
    assert login_response.status_code == 200
    return login_response.json()["authorization"]


def test_list_products():
    response = requests.get(BASE_URL + "/produtos")
    body = response.json()

    assert response.status_code == 200
    assert "quantidade" in body
    assert "produtos" in body
    assert isinstance(body["produtos"], list)


def test_create_product_as_admin():
    token = create_admin_token()
    payload = new_product_payload()
    response = create_product(token, payload)
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body


def test_create_product_without_token():
    payload = new_product_payload()
    response = requests.post(BASE_URL + "/produtos", json=payload)

    assert response.status_code == 401


def test_create_product_as_non_admin_returns_forbidden():
    user_payload = new_user_payload(administrador="false")
    create_response = create_user(user_payload)
    assert create_response.status_code == 201

    login_response = do_login({"email": user_payload["email"], "password": user_payload["password"]})
    assert login_response.status_code == 200
    token = login_response.json()["authorization"]

    payload = new_product_payload()
    response = create_product(token, payload)

    assert response.status_code == 403


def test_get_product_by_id():
    token = create_admin_token()
    payload = new_product_payload()
    creation_response = create_product(token, payload)
    assert creation_response.status_code == 201
    product_id = creation_response.json()["_id"]

    response = requests.get(BASE_URL + f"/produtos/{product_id}")
    body = response.json()

    assert response.status_code == 200
    assert body["_id"] == product_id
    assert body["nome"] == payload["nome"]


def test_update_product_as_admin():
    token = create_admin_token()
    payload = new_product_payload()
    creation_response = create_product(token, payload)
    assert creation_response.status_code == 201
    product_id = creation_response.json()["_id"]

    updated_payload = {
        "nome": payload["nome"] + " Atualizado",
        "preco": payload["preco"],
        "descricao": payload["descricao"],
        "quantidade": payload["quantidade"],
    }

    response = requests.put(BASE_URL + f"/produtos/{product_id}", json=updated_payload, headers={"Authorization": token})
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Registro alterado com sucesso"


def test_delete_product_as_admin():
    token = create_admin_token()
    payload = new_product_payload()
    creation_response = create_product(token, payload)
    assert creation_response.status_code == 201
    product_id = creation_response.json()["_id"]

    response = requests.delete(BASE_URL + f"/produtos/{product_id}", headers={"Authorization": token})
    body = response.json()

    assert response.status_code == 200
    assert "Registro excluído" in body["message"]
