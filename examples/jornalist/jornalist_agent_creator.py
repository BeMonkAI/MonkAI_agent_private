from core import MonkaiAgentCreator,TransferTriageAgentCreator
from core import Agent
import core.security as security
import os
import requests

class JornalistAgentCreator(TransferTriageAgentCreator):

    def __init__(self):
        super().__init__()
        self.__jornalist_agent = Agent(name="Jornalist Agent",
           instructions="""Você é um agente encarregado de resumir las notícia do dia lidas nos Jornal especificos.
            """,
            functions=[  
                        self.read_news,
                      ])
        
    def get_agent(self):
        """
        Returns the Jornalist Agent.
        """
        return self.__jornalist_agent
    
    def get_agent_briefing(self):
        return "Você é um agente encarregado de resumir las notícia do dia lidas nos Jornal especificos"
    
    def read_news(self):
        """
        Read the news.
        """
        news = requests.get("https://g1.globo.com/").text
        return f"As noticias a resumir são: {news[:120000]}"