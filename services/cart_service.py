from services.api_client import get, post, delete


def list_carts():
    return get("/carrinhos")


def create_cart(token, product_id, quantity=1):
    return post(
        "/carrinhos",
        json={"produtos": [{"idProduto": product_id, "quantidade": quantity}]},
        headers={"Authorization": token},
    )


def get_cart_by_id(cart_id):
    return get(f"/carrinhos/{cart_id}")


def conclude_purchase(token):
    return delete("/carrinhos/concluir-compra", headers={"Authorization": token})


def cancel_purchase(token):
    return delete("/carrinhos/cancelar-compra", headers={"Authorization": token})
