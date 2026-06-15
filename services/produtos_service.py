from services.api_client import get, post, put, delete


class ProdutosService:
    @staticmethod
    def list_all():
        """Listar todos os produtos."""
        return get("/produtos")

    @staticmethod
    def create(token, payload):
        """Criar um novo produto (requer token de admin)."""
        return post("/produtos", json=payload, headers={"Authorization": token})

    @staticmethod
    def get_by_id(product_id):
        """Buscar produto por ID."""
        return get(f"/produtos/{product_id}")

    @staticmethod
    def update(product_id, payload, token):
        """Atualizar um produto existente (requer token de admin)."""
        return put(f"/produtos/{product_id}", json=payload, headers={"Authorization": token})

    @staticmethod
    def delete(product_id, token):
        """Deletar um produto (requer token de admin)."""
        return delete(f"/produtos/{product_id}", headers={"Authorization": token})
