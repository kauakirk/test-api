from services.usuarios_service import UsuariosService
from services.produtos_service import ProdutosService
from utils.payloads import new_user_payload, new_product_payload
from utils.auth import admin_token


def test_list_products():
    response = ProdutosService.list_all()
    body = response.json()

    assert response.status_code == 200
    assert "quantidade" in body
    assert "produtos" in body
    assert isinstance(body["produtos"], list)


def test_create_product_as_admin():
    token = admin_token()
    payload = new_product_payload()
    response = ProdutosService.create(token, payload)
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body


def test_create_product_without_token():
    payload = new_product_payload()
    response = ProdutosService.create("", payload)

    assert response.status_code == 401


def test_create_product_as_non_admin_returns_forbidden():
    user_payload = new_user_payload(administrador="false")
    create_response = UsuariosService.create(user_payload)
    assert create_response.status_code == 201

    login_response = UsuariosService.login({"email": user_payload["email"], "password": user_payload["password"]})
    assert login_response.status_code == 200
    token = login_response.json()["authorization"]

    payload = new_product_payload()
    response = ProdutosService.create(token, payload)

    assert response.status_code == 403


def test_get_product_by_id():
    token = admin_token()
    payload = new_product_payload()
    creation_response = ProdutosService.create(token, payload)
    assert creation_response.status_code == 201
    product_id = creation_response.json()["_id"]

    response = ProdutosService.get_by_id(product_id)
    body = response.json()

    assert response.status_code == 200
    assert body["_id"] == product_id
    assert body["nome"] == payload["nome"]


def test_update_product_as_admin():
    token = admin_token()
    payload = new_product_payload()
    creation_response = ProdutosService.create(token, payload)
    assert creation_response.status_code == 201
    product_id = creation_response.json()["_id"]

    updated_payload = {
        "nome": payload["nome"] + " Atualizado",
        "preco": payload["preco"],
        "descricao": payload["descricao"],
        "quantidade": payload["quantidade"],
    }

    response = ProdutosService.update(product_id, updated_payload, token)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Registro alterado com sucesso"


def test_delete_product_as_admin():
    token = admin_token()
    payload = new_product_payload()
    creation_response = ProdutosService.create(token, payload)
    assert creation_response.status_code == 201
    product_id = creation_response.json()["_id"]

    response = ProdutosService.delete(product_id, token)
    body = response.json()

    assert response.status_code == 200
    assert "Registro excluído" in body["message"]

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
