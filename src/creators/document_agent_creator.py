
from swarm import Agent
from llama_index.core import StorageContext, load_index_from_storage
from creators.monkai_agent_creator import MonkaiAgentCreator


class DocumentAgentCreator(MonkaiAgentCreator):
    def __init__(self):
        super().__init__()
        self.storage_ctx = StorageContext.from_defaults(persist_dir="documents/examples/vstorage")
        self.index = load_index_from_storage(storage_context=self.storage_ctx)
        self.agent =  Agent(
                name="Document Agent",
                instructions="""Você é um agente responsavel por tirar dúvidas do usuário sobre um documento.
                            Instruções:

                            1.Interprete a pergunta do usuário
                            2.Acesse o documento para responder a pergunta
                            3.Crie uma resposta para a pergunta do usuário
                """,
                functions=[self.rag_agent_documento],
                external_content=True
            )

    
    

    def get_agent(self) -> Agent:
        """
        Get the POC Agent. 

        Returns: 
            Agent: The POC Agent.
        """
        return self.agent
    
    def get_agent_briefing(self) -> str:
        return "Você é um agente responsavel por tirar dúvidas do usuário sobre a empresa BYX Capital utilizando as informações do documento da empresa."
    
   
    def rag_agent_documento(self, question: str) -> str:
        
        try:
            self.query_engine = self.index.as_query_engine(
                    include_text=True,
                    similarity_top_k=5
                )
            
            response = self.query_engine.query(f"Procura a informação que melhor responde á pergunta {question}")
            return response.response
        except Exception as e:
            return "Sua pergunta não pode ser respondida."
        
              
        
    