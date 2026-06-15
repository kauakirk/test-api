import requests

BASE_URL = "https://compassuol.serverest.dev"


def get(path, **kwargs):
    return requests.get(BASE_URL + path, **kwargs)


def post(path, json=None, headers=None):
    return requests.post(BASE_URL + path, json=json, headers=headers)


def put(path, json=None, headers=None):
    return requests.put(BASE_URL + path, json=json, headers=headers)


def delete(path, headers=None):
    return requests.delete(BASE_URL + path, headers=headers)
