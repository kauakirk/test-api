from services.api_client import get, post, delete


class CarrinhosService:
    @staticmethod
    def list_all():
        """Listar todos os carrinhos."""
        return get("/carrinhos")

    @staticmethod
    def create(token, product_id, quantity=1):
        """Criar um novo carrinho com produtos (requer token do usuário)."""
        return post(
            "/carrinhos",
            json={"produtos": [{"idProduto": product_id, "quantidade": quantity}]},
            headers={"Authorization": token},
        )

    @staticmethod
    def get_by_id(cart_id):
        """Buscar carrinho por ID."""
        return get(f"/carrinhos/{cart_id}")

    @staticmethod
    def conclude_purchase(token):
        """Concluir a compra e deletar o carrinho (requer token do usuário)."""
        return delete("/carrinhos/concluir-compra", headers={"Authorization": token})

    @staticmethod
    def cancel_purchase(token):
        """Cancelar a compra e reabastecer estoque (requer token do usuário)."""
        return delete("/carrinhos/cancelar-compra", headers={"Authorization": token})
