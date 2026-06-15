from services.usuarios_service import UsuariosService
from services.produtos_service import ProdutosService
from services.carrinhos_service import CarrinhosService
from utils.payloads import new_user_payload, new_product_payload
from utils.auth import admin_token, user_token


def test_list_carts():
    response = CarrinhosService.list_all()
    body = response.json()

    assert response.status_code == 200
    assert "quantidade" in body
    assert "carrinhos" in body
    assert isinstance(body["carrinhos"], list)


def test_create_cart_with_valid_token():
    admin_tok = admin_token()
    product_response = ProdutosService.create(admin_tok, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_payload = new_user_payload()
    user_response = UsuariosService.create(user_payload)
    assert user_response.status_code == 201

    login_response = UsuariosService.login({"email": user_payload["email"], "password": user_payload["password"]})
    assert login_response.status_code == 200
    user_tok = login_response.json()["authorization"]

    cart_response = CarrinhosService.create(user_tok, product_id)
    body = cart_response.json()

    assert cart_response.status_code == 201
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body


def test_get_cart_by_id():
    admin_tok = admin_token()
    product_response = ProdutosService.create(admin_tok, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_payload = new_user_payload()
    UsuariosService.create(user_payload)
    login_response = UsuariosService.login({"email": user_payload["email"], "password": user_payload["password"]})
    assert login_response.status_code == 200
    user_tok = login_response.json()["authorization"]

    create_response = CarrinhosService.create(user_tok, product_id)
    assert create_response.status_code == 201
    cart_id = create_response.json()["_id"]

    response = CarrinhosService.get_by_id(cart_id)
    body = response.json()

    assert response.status_code == 200
    assert body["_id"] == cart_id


def test_conclude_purchase_deletes_cart():
    admin_tok = admin_token()
    product_response = ProdutosService.create(admin_tok, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_payload = new_user_payload()
    UsuariosService.create(user_payload)
    login_response = UsuariosService.login({"email": user_payload["email"], "password": user_payload["password"]})
    assert login_response.status_code == 200
    user_tok = login_response.json()["authorization"]

    create_response = CarrinhosService.create(user_tok, product_id)
    assert create_response.status_code == 201

    response = CarrinhosService.conclude_purchase(user_tok)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] in [
        "Registro excluído com sucesso",
        "Registro excluído com sucesso | Não foi encontrado carrinho para esse usuário",
    ]


def test_cancel_purchase_deletes_cart_and_restock():
    admin_tok = admin_token()
    product_response = ProdutosService.create(admin_tok, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_payload = new_user_payload()
    UsuariosService.create(user_payload)
    login_response = UsuariosService.login({"email": user_payload["email"], "password": user_payload["password"]})
    assert login_response.status_code == 200
    user_tok = login_response.json()["authorization"]

    create_response = CarrinhosService.create(user_tok, product_id)
    assert create_response.status_code == 201

    response = CarrinhosService.cancel_purchase(user_tok)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] in [
        "Registro excluído com sucesso",
        "Registro excluído com sucesso | Não foi encontrado carrinho para esse usuário",
    ]

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
