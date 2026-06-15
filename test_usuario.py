import requests


ENDPOINT = 'https://compassuol.serverest.dev/'
payload = {
        "email": "fulano@qa.com",
        "password": "teste",
    }


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_login():
    response = requests.post(
        f"{ENDPOINT}/login",
        json=payload
    )
    
    body = response.json()
    print(body
          )
    assert response.status_code == 200
    assert body ["message"]  == "Login realizado com sucessos"