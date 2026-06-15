from services.api_client import get, post, put, delete


class UsuariosService:
    @staticmethod
    def create(payload):
        """Criar um novo usuário."""
        return post("/usuarios", json=payload)

    @staticmethod
    def login(payload):
        """Fazer login com credenciais de usuário."""
        return post("/login", json=payload)

    @staticmethod
    def list_all():
        """Listar todos os usuários."""
        return get("/usuarios")

    @staticmethod
    def get_by_id(user_id):
        """Buscar usuário por ID."""
        return get("/usuarios", params={"_id": user_id})

    @staticmethod
    def update(user_id, payload):
        """Atualizar um usuário existente."""
        return put(f"/usuarios/{user_id}", json=payload)

    @staticmethod
    def delete(user_id):
        """Deletar um usuário."""
        return delete(f"/usuarios/{user_id}")
