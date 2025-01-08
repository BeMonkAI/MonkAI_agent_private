from abc import ABC, abstractmethod
from .types import Agent

class MonkaiAgentCreator(ABC):


    @abstractmethod
    def get_agent(self)->Agent:
        pass

    @abstractmethod
    def get_agent_briefing(self)->str:
        pass


class TransferTriageAgentCreator(MonkaiAgentCreator):
    """
    A class to create and manage a triage agent.

    """

    __triage_agent = None
    """
    The triage agent instance.
    
    """

    @property
    def set_triage_agent(self, triage_agent: Agent):
        """
        Sets the triage agent.

        Args:
            triage_agent (Agent): The triage agent to be set.
        """
        self.__triage_agent = triage_agent

    def transfer_to_triagem(self):
        """
        Transfers the conversation to the  triage agent.

        Args:
            agent (Agent): The agent to transfer the conversation to.
        """
        return self.__triage_agent