from services.usuarios_service import UsuariosService
from utils.payloads import new_user_payload


def admin_token():
    """Criar um token de admin para testes."""
    payload = new_user_payload(administrador="true")
    create_response = UsuariosService.create(payload)
    assert create_response.status_code == 201

    login_response = UsuariosService.login({"email": payload["email"], "password": payload["password"]})
    assert login_response.status_code == 200
    return login_response.json()["authorization"]


def user_token():
    """Criar um token de usuário comum para testes."""
    payload = new_user_payload(administrador="false")
    create_response = UsuariosService.create(payload)
    assert create_response.status_code == 201

    login_response = UsuariosService.login({"email": payload["email"], "password": payload["password"]})
    assert login_response.status_code == 200
    return login_response.json()["authorization"]
