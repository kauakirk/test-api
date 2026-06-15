from services.api_client import get, post, put, delete


def list_products():
    return get("/produtos")


def create_product(token, payload):
    return post("/produtos", json=payload, headers={"Authorization": token})


def get_product_by_id(product_id):
    return get(f"/produtos/{product_id}")


def update_product(product_id, payload, token):
    return put(f"/produtos/{product_id}", json=payload, headers={"Authorization": token})


def delete_product(product_id, token):
    return delete(f"/produtos/{product_id}", headers={"Authorization": token})
