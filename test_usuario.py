import requests
import uuid


ENDPOINT = 'https://compassuol.serverest.dev'



def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_get_users():
    response = get_users()

    body = response.json()

    assert response.status_code == 200
    assert "quantidade" in body
    assert "usuarios" in body
    assert isinstance(body["usuarios"], list)



def test_can_create_user():
    user_payload = new_user_payload()
    response = post_create_user(user_payload)
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body 



def test_can_create_user_and_login():
    user_payload = new_user_payload()

    create_response = post_create_user(user_payload)

    assert create_response.status_code == 201

    login_payload = {
        "email": user_payload["email"],
        "password": user_payload["password"]
    }

    login_response = post_login(login_payload)

    body = login_response.json()

    assert login_response.status_code == 200
    assert body["message"] == "Login realizado com sucesso"
    assert "authorization" in body

def test_can_create_and_delete_user():
    user_payload = new_user_payload()

    create_response = post_create_user(user_payload)

    assert create_response.status_code == 201

    user_id = create_response.json()["_id"]
    delete_response = delete_user(user_id)

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Registro excluído com sucesso"

def test_can_delete_nonexistent_user():
    delete_response = delete_user("nonexistent_user_id")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Nenhum registro excluído"



def delete_user(user_id):
    return requests.delete(ENDPOINT + f"/usuarios/{user_id}")

def post_login(payload):
    return requests.post(ENDPOINT + "/login", json=payload)

def get_users():
    return requests.get(ENDPOINT + "/usuarios")

def post_create_user(payload):
    return requests.post(ENDPOINT + "/usuarios", json=payload)

def new_user_payload():
    unique_id = uuid.uuid4().hex
    return{
        "nome": f"Fulano{unique_id}",
        "email": f"fulano_{unique_id}@gmail.com",
        "password": "123",
        "administrador": "false"

    }


    