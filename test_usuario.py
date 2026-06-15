import requests


ENDPOINT = 'https://compassuol.serverest.dev/'



def test_can_call_endpoint():
    response = request.get(ENDPOINT)
    assert response.status_code == 200





