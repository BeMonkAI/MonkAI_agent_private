
from .monkai_agent_creator import MonkaiAgentCreator
from .types import Agent

class TriageAgentCreator(MonkaiAgentCreator):
    def __init__(self, agents_creator:list[MonkaiAgentCreator]):
       self.agents_creator = agents_creator
       self.__build_agent()

    def __create_transfer_function(self, agent_creator:MonkaiAgentCreator):
        def transfer_function():
            return agent_creator.get_agent()
        transfer_function.__name__ = f"transfer_to_{agent_creator.get_agent().name.replace(' ', '_')}"
        return transfer_function

    def __build_agent(self):
        instructions = ""
        functions = []
        print("Building triage agent")
        print(self.agents_creator)
        for agent_creator in self.agents_creator:

            functions.append(self.__create_transfer_function(agent_creator))
            agent = agent_creator.get_agent()
            print(agent.name)
            print(agent_creator.get_agent_briefing())
            instructions += f"- **Transfer to `{agent.name}`** if the user's query is about: {agent_creator.get_agent_briefing()}\n\n"
        self.triage_agent = Agent(
            name="Triage Agent",
            instructions=f"""
            Determine which agent is most suitable to handle the user's request and transfer the conversation to that agent.

            Instructions:

                {instructions}
                
            """,
            functions=functions
        )

    def get_agent(self)->Agent:
         # Define the triage agent manually
        return self.triage_agent

    def get_agent_briefing(self)->str:
        return "Review the user's query and transfer the conversation to the appropriate agent."