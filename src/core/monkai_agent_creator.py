from abc import ABC, abstractmethod
#from core import Agent
from .types import Agent

class MonkaiAgentCreator(ABC):


    @abstractmethod
    def get_agent(self)->Agent:
        pass

    @abstractmethod
    def get_agent_briefing(self)->str:
        pass


class TransferTriaggenAgentCreator(MonkaiAgentCreator):
    """
    A class to create and manage a triaggen agent.

    Attributes:
        __triaggent_agent (Agent): The triaggen agent instance.
    """

    __triaggent_agent = None

    @property
    def set_triaggent_agent(self, triaggent_agent: Agent):
        """
        Sets the triaggen agent.

        Args:
            triaggent_agent (Agent): The triaggen agent to be set.
        """
        self.__triaggent_agent = triaggent_agent

    def transfer_to_triagem(self):
        """
        Transfers the conversation to the  triaggent agent.

        Args:
            agent (Agent): The agent to transfer the conversation to.
        """
        return self.__triaggent_agent