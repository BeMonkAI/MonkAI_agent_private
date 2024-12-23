from swarm import Agent
from llama_index.core import StorageContext, load_index_from_storage
from creators.monkai_agent_creator import MonkaiAgentCreator


class BYXAgentCreator(MonkaiAgentCreator):
    def __init__(self):
        super().__init__()
        self.storage_ctx = StorageContext.from_defaults(persist_dir="documents/vstorage")
        self.index = load_index_from_storage(storage_context=self.storage_ctx)
        self.agent =  Agent(
                name="Customer Support BYX Agent",
                instructions="""Você é um agente responsavel por tirar dúvidas do usuário sobre a empresa BYX Capital utilizando as informações do documento da empresa.
                            
                            Guardrails:
                            - Não responder perguntas que não esteja no contexto.
                """,
                functions=[self.rag_agent_byx, self.transfer_analista_byx_customer_support],
                external_content=True
            )

    
    def transfer_analista_byx_customer_support(resumo: str):
        """
        Transferir a conversa para um analista humano de suporte ao cliente da empresa BYX Capital caso o agente de suporte ao cliente da empresa BYX Capital não saiba responder a pergunta do usuário.
        
        Args:
            resumo (_type_): Resumo da conversa entre o usuário e o agente de suporte ao cliente da empresa BYX Capital.
        
        return: 
            print(f'Transferindo para um atendente humano para ajudar com sua dúvida: {resumo}')
        """
        return resumo

    def get_agent(self) -> Agent:
        """
        Get the POC Agent. 

        Returns: 
            Agent: The POC Agent.
        """
        return self.agent
    
    def get_agent_briefing(self) -> str:
        return "Você é um agente responsavel por tirar dúvidas do usuário sobre a empresa BYX Capital utilizando as informações do documento da empresa."
    
   
    def rag_agent_byx(self, question: str) -> str:
        """Acessar o documento da empresa BYX Capital e responder a pergunta do usuário. O Grupo BYX é um ecossistema de crédito colateralizado, 
        que oferece infraestrutura completa para integrar originadores de crédito e alocadores de capital com transparência, previsibilidade e segurança.
        O documento é um whitepaper que relata o FAQ das principais dúvidas sobre a empresa BYX Capital.
        
        Args:
            query (_type_): Pergunta do usuário sobre a empresa BYX Capital.

        Returns:
            _type_: Resposta encontrada no documento da empresa BYX Capital.
        """      
        try:
            self.query_engine = self.index.as_query_engine(
                    include_text=True,
                    similarity_top_k=5
                )
            
            response = self.query_engine.query(f"Procura a informação que melhor responde á pergunta {question}")
            return response.response
        except Exception as e:
            return "Sua pergunta não pode ser respondida."
        
      
    @property
    def valid_phone(self) -> list[str]: 
        return ["5521998177496","5581991850288","5521983270002","5521999062808", "5511998402316"]            
        
    