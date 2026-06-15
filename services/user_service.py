from services.api_client import get, post, put, delete


def create_user(payload):
    return post("/usuarios", json=payload)


def login(payload):
    return post("/login", json=payload)


def get_users():
    return get("/usuarios")


def get_user_by_id(user_id):
    return get("/usuarios", params={"_id": user_id})


def update_user(user_id, payload):
    return put(f"/usuarios/{user_id}", json=payload)


def delete_user(user_id):
    return delete(f"/usuarios/{user_id}")
