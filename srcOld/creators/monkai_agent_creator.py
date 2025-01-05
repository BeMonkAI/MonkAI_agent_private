from abc import ABC, abstractmethod
from swarm import Agent

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

    def __init__(self, triaggent_agent:Agent = None):
        """
        Initializes the triaggen agent creator.

        Args:
            agents_creator (list[MonkaiAgentCreator]): The list of agents to be created.
        """
        self.__triaggent_agent = triaggent_agent

    @property
    def triaggent_agent(self):
        """
        Sets the triaggen agent.

        Args:
            triaggent_agent (Agent): The triaggen agent to be set.
        """
        return self.__triaggent_agent

    @triaggent_agent.setter
    def triaggent_agent(self, triaggent_agent: Agent):
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
        return self.triaggent_agent