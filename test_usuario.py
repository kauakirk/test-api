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

def test_can_login():
    payload = login_payload()
    response = post_login(payload)
    
    body = response.json()
    print(body
          )
    assert response.status_code == 200
    assert body ["message"]  == "Login realizado com sucesso"

def test_can_create_user():
    payload = new_user_payload()
    response = post_create_user(payload)
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body 



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
def login_payload():
    return {
        "email": "fulano@qa.com",
        "password": "teste"
    }

    