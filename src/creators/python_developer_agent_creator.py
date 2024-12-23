
from creators.monkai_agent_creator import MonkaiAgentCreator
from swarm import Agent
import os

#menssagens = [SystemMessage,SystemMessage,InstructionMessage1,InstructionMessage2, InstructionMessage3, .....]

class PythonDeveloperAgentCreator(MonkaiAgentCreator):
    def __init__(self):
        self.agent = Agent(
            name="Python Developer Agent",
           instructions="""Você é um desenvolvedor Python e deve criar um código Python a partir de um texto fornecido pelo usuário.
            Instruções:

                1. Interprete o texto do usuário para entender os requisitos do código Python a ser gerado.
                2. Gere o código Python, definindo classes conforme necessário e seguindo boas práticas de orientação a objetos. Garanta que o código gerado seja corretamente documentado.
                3. Verifique se existe um endereço fornecido pelo usuário na mensagem. Se nenhum endereço for fornecido, use a pasta atual.
                4. Crie um arquivo .py na pasta especificada.
                5. Defina uma classe no arquivo criado com as funcionalidades que atendem às condições especificadas pelo usuário.
            """,
            functions=[  
                        self.verify_address,    
                        self.create_python_file,
                        self.write_code_in_file
                      ])

    def verify_address(self, address):
        if not address:
            return os.getcwd()
        if not os.path.isdir(address):
            return f"Endereço {address} não é valido."
        return address

    def create_python_file(self, path, file_name):
        complete_path = os.path.join(path, file_name)
        with open(complete_path, 'w') as f:
            f.write('')

    def write_code_in_file(self,path, file_name, code):
        """
        Write the code in the file.
        """
        complete_path = os.path.join(path, file_name)
        with open(complete_path, 'w') as f:
            f.write(code)

    def replace_code_in_file(self, path, file_name, code):
        """
        Replace the code in the file.
        """
        complete_path = os.path.join(path, file_name)
        with open(complete_path, 'w') as f:
            f.write(code)

    def get_agent(self) -> Agent:
        """
        Returns the Python Developer Agent.
        """
        return self.agent
    
    def get_agent_briefing(self) -> str:
        return "Você é um desenvolvedor Python e deve criar um código Python a partir de um texto fornecido pelo usuário."

            