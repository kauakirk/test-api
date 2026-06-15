from services.user_service import create_user, login
from utils.payloads import new_user_payload


def admin_token():
    payload = new_user_payload(administrador="true")
    create_response = create_user(payload)
    assert create_response.status_code == 201

    login_response = login({"email": payload["email"], "password": payload["password"]})
    assert login_response.status_code == 200
    return login_response.json()["authorization"]


def user_token():
    payload = new_user_payload(administrador="false")
    create_response = create_user(payload)
    assert create_response.status_code == 201

    login_response = login({"email": payload["email"], "password": payload["password"]})
    assert login_response.status_code == 200
    return login_response.json()["authorization"]
