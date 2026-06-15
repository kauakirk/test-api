import requests


ENDPOINT = 'https://compassuol.serverest.dev/'

response = requests.get(ENDPOINT)
print(response)
print(response.status_code)



