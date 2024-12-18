class Profesor:
    def __init__(self, nome, idade, instituicao_de_ensino):
        """
        Inicializa uma instância da classe Profesor.

        :param nome: Nome do professor
        :param idade: Idade do professor
        :param instituicao_de_ensino: Nome da instituição de ensino
        """
        self.nome = nome
        self.idade = idade
        self.instituicao_de_ensino = instituicao_de_ensino
    
    def verificar_instituicao(self):
        """
        Verifica se a instituição de ensino contém a palavra 'Federal'.

        :return: True se contém 'Federal', caso contrário False
        """
        return "Federal" in self.instituicao_de_ensino