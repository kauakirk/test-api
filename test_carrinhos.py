import requests
import uuid

BASE_URL = "https://compassuol.serverest.dev"


def new_user_payload(administrador="false"):
    unique_id = uuid.uuid4().hex
    return {
        "nome": f"Carrinho User {unique_id}",
        "email": f"carrinho_user_{unique_id}@qa.com",
        "password": "teste123",
        "administrador": administrador,
    }


def new_product_payload():
    unique_id = uuid.uuid4().hex
    return {
        "nome": f"Carrinho Produto {unique_id}",
        "preco": 100,
        "descricao": "Produto para carrinho",
        "quantidade": 10,
    }


def create_user(payload):
    return requests.post(BASE_URL + "/usuarios", json=payload)


def do_login(payload):
    return requests.post(BASE_URL + "/login", json=payload)


def create_admin_token():
    admin_payload = new_user_payload(administrador="true")
    create_response = create_user(admin_payload)
    assert create_response.status_code == 201

    login_response = do_login({"email": admin_payload["email"], "password": admin_payload["password"]})
    assert login_response.status_code == 200
    return login_response.json()["authorization"]


def create_product(token, payload):
    return requests.post(BASE_URL + "/produtos", json=payload, headers={"Authorization": token})


def create_cart(token, product_id, quantity=1):
    return requests.post(BASE_URL + "/carrinhos", json={"produtos": [{"idProduto": product_id, "quantidade": quantity}]}, headers={"Authorization": token})


def test_list_carts():
    response = requests.get(BASE_URL + "/carrinhos")
    body = response.json()

    assert response.status_code == 200
    assert "quantidade" in body
    assert "carrinhos" in body
    assert isinstance(body["carrinhos"], list)


def test_create_cart_with_valid_token():
    admin_token = create_admin_token()
    product_response = create_product(admin_token, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_payload = new_user_payload()
    user_response = create_user(user_payload)
    assert user_response.status_code == 201

    login_response = do_login({"email": user_payload["email"], "password": user_payload["password"]})
    assert login_response.status_code == 200
    user_token = login_response.json()["authorization"]

    cart_response = create_cart(user_token, product_id)
    body = cart_response.json()

    assert cart_response.status_code == 201
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body


def test_get_cart_by_id():
    admin_token = create_admin_token()
    product_response = create_product(admin_token, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_payload = new_user_payload()
    create_user(user_payload)
    login_response = do_login({"email": user_payload["email"], "password": user_payload["password"]})
    assert login_response.status_code == 200
    user_token = login_response.json()["authorization"]

    create_response = create_cart(user_token, product_id)
    assert create_response.status_code == 201
    cart_id = create_response.json()["_id"]

    response = requests.get(BASE_URL + f"/carrinhos/{cart_id}")
    body = response.json()

    assert response.status_code == 200
    assert body["_id"] == cart_id


def test_conclude_purchase_deletes_cart():
    admin_token = create_admin_token()
    product_response = create_product(admin_token, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_payload = new_user_payload()
    create_user(user_payload)
    login_response = do_login({"email": user_payload["email"], "password": user_payload["password"]})
    assert login_response.status_code == 200
    user_token = login_response.json()["authorization"]

    create_response = create_cart(user_token, product_id)
    assert create_response.status_code == 201

    response = requests.delete(BASE_URL + "/carrinhos/concluir-compra", headers={"Authorization": user_token})
    body = response.json()

    assert response.status_code == 200
    assert body["message"] in [
        "Registro excluído com sucesso",
        "Registro excluído com sucesso | Não foi encontrado carrinho para esse usuário",
    ]


def test_cancel_purchase_deletes_cart_and_restock():
    admin_token = create_admin_token()
    product_response = create_product(admin_token, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_payload = new_user_payload()
    create_user(user_payload)
    login_response = do_login({"email": user_payload["email"], "password": user_payload["password"]})
    assert login_response.status_code == 200
    user_token = login_response.json()["authorization"]

    create_response = create_cart(user_token, product_id)
    assert create_response.status_code == 201

    response = requests.delete(BASE_URL + "/carrinhos/cancelar-compra", headers={"Authorization": user_token})
    body = response.json()

    assert response.status_code == 200
    assert body["message"] in [
        "Registro excluído com sucesso",
        "Registro excluído com sucesso | Não foi encontrado carrinho para esse usuário",
    ]
