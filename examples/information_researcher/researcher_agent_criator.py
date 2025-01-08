from core.monkai_agent_creator import MonkaiAgentCreator, TransferTriageAgentCreator
from core.types import Agent
import core.security as security
import os
import requests

class ResearcherAgentCriator(TransferTriageAgentCreator):
    def __init__(self):
        super().__init__()
        self.__researcher_agent = Agent(name="Researcher Agent",
           instructions="""Você é um agente encargado de procurar informação na internet referente a um pedido do usuario. 
             Responda diretamente a pergunta do usuario e envie junto as referencias validas.
            Lembra sempre  verificar uma a uma  as referencias utilizadas.
            """,
            functions=[  
                        self.check_reference,
                      ])
        
    def check_reference(self, reference:str):
        """
        Check if the reference is valid.
        """
        if not reference:
            return f"Referencia {reference} invalida."
        if requests.get(reference).status_code != 200:
            return f"Referencia {reference} invalida"
        return f"Referencia {reference} valida"
    
    def get_agent(self) -> Agent:
        """
        Returns the Researcher Agent.
        """
        return self.__researcher_agent
    
    def get_agent_briefing(self):
        return "Você é um agente encargado de procurar informação na internet referente a um pedido do usuario e retornar referencias validas."