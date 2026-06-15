import requests
import uuid

BASE_URL = "https://compassuol.serverest.dev"


def new_user_payload(administrador="false"):
    unique_id = uuid.uuid4().hex
    return {
        "nome": f"Login User {unique_id}",
        "email": f"login_user_{unique_id}@qa.com",
        "password": "teste123",
        "administrador": administrador,
    }


def create_user(payload):
    return requests.post(BASE_URL + "/usuarios", json=payload)


def do_login(payload):
    return requests.post(BASE_URL + "/login", json=payload)


def test_login_with_valid_credentials():
    user_payload = new_user_payload()
    create_response = create_user(user_payload)
    assert create_response.status_code == 201

    login_response = do_login({"email": user_payload["email"], "password": user_payload["password"]})
    body = login_response.json()

    assert login_response.status_code == 200
    assert body["message"] == "Login realizado com sucesso"
    assert "authorization" in body


def test_login_with_wrong_password():
    user_payload = new_user_payload()
    create_response = create_user(user_payload)
    assert create_response.status_code == 201

    login_response = do_login({"email": user_payload["email"], "password": "senhaerrada"})
    body = login_response.json()

    assert login_response.status_code == 401
    assert body["message"] == "Email e/ou senha inválidos"


def test_login_with_nonexistent_email():
    login_response = do_login({"email": f"nao_existe_{uuid.uuid4().hex}@qa.com", "password": "senha123"})
    body = login_response.json()

    assert login_response.status_code == 401
    assert body["message"] == "Email e/ou senha inválidos"


def test_login_with_empty_fields():
    login_response = do_login({"email": "", "password": ""})
    assert login_response.status_code == 400
