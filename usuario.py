class Usuario:
    """
      Classe que representa um usuário.
    """
    def __init__(self, nome, email=None, telefone=None, id=None):
        """
        Inicializa uma nova instância da classe Usuario.

        Args:
            nome (str): O nome do usuário.
            email (str, opcional): O email do usuário.
            telefone (str, opcional): O telefone do usuário.
            id (str, opcional): O ID do usuário.
        """
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
    """
    Exemplo de uso. Verifica se os usuários são válidos. 
    Cria três instâncias da classe Usuario com diferentes combinações de atributos e imprime o resultado da validação de cada usuário.
    """
    usuario1 = Usuario(nome="João", email="joao@example.com")
    usuario2 = Usuario(nome="Maria", telefone="123456789")
    usuario3 = Usuario(nome="Pedro")

    print(usuario1.validacao())  # True
    print(usuario2.validacao())  # True
    print(usuario3.validacao())  # False