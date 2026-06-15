from services.usuarios_service import UsuariosService
from utils.payloads import new_user_payload


def test_login_with_valid_credentials():
    user_payload = new_user_payload()
    create_response = UsuariosService.create(user_payload)
    assert create_response.status_code == 201

    login_response = UsuariosService.login({"email": user_payload["email"], "password": user_payload["password"]})
    body = login_response.json()

    assert login_response.status_code == 200
    assert body["message"] == "Login realizado com sucesso"
    assert "authorization" in body


def test_login_with_wrong_password():
    user_payload = new_user_payload()
    create_response = UsuariosService.create(user_payload)
    assert create_response.status_code == 201

    login_response = UsuariosService.login({"email": user_payload["email"], "password": "senhaerrada"})
    body = login_response.json()

    assert login_response.status_code == 401
    assert body["message"] == "Email e/ou senha inválidos"


def test_login_with_nonexistent_email():
    import uuid
    login_response = UsuariosService.login({"email": f"nao_existe_{uuid.uuid4().hex}@qa.com", "password": "senha123"})
    body = login_response.json()

    assert login_response.status_code == 401
    assert body["message"] == "Email e/ou senha inválidos"


def test_login_with_empty_fields():
    login_response = UsuariosService.login({"email": "", "password": ""})
    assert login_response.status_code == 400
