class Usuario:
    def __init__(self, nome, email=None, telefone=None, id=None):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.id = id

    def validacao(self):
        """
        Verifica se o usuário tem pelo menos o email ou o telefone.

        Returns:
            bool: True se o usuário tem pelo menos o email ou o telefone, caso contrário False.
        """
        return bool(self.email or self.telefone)

# Exemplo de uso
if __name__ == "__main__":
    usuario1 = Usuario(nome="João", email="joao@example.com")
    usuario2 = Usuario(nome="Maria", telefone="123456789")
    usuario3 = Usuario(nome="Pedro")

    print(usuario1.validacao())  # True
    print(usuario2.validacao())  # True
    print(usuario3.validacao())  # False