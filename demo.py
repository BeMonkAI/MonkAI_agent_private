from core import AgentManager
import asyncio
from core.triage_agent_creator import TriageAgentCreator
from core.repl import run_demo_loop
import json
from bson import ObjectId
#from monkai_shared import config
import config 
from openai import AzureOpenAI



if __name__ == '__main__': 
    #from dotenv import load_dotenv
    #load_dotenv() 
    from examples.python_developer.python_developer_agent_creator import PythonDeveloperAgentCreator
    from examples.information_researcher.researcher_agent_criator import ResearcherAgentCriator
    from examples.jornalist.jornalist_agent_creator import JornalistAgentCreator
    from examples.secure_calculator.calculator_agents_creator import CalculatorAgentCriator
    #print("PDFAgent")    
    #services = Services()
    #mluser_service = services.get_mluser_service()
    #user = mluser_service.get_user(ObjectId("672286bdc37ef0e984a8a455"))
    #contents = services.get_content_service().get_contents_by_user(user)
    agents_creators = []
    agents_creators.append(PythonDeveloperAgentCreator())
    agents_creators.append(ResearcherAgentCriator())
    agents_creators.append(JornalistAgentCreator())
    agents_creators.append(CalculatorAgentCriator("invalid_user"))
    client=AzureOpenAI(api_key=config.OPENAI_API_KEY_BRASILSOUTH, api_version=config.OPENAI_API_VERSION, azure_endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH)
    agent_manager = AgentManager(client=client, agents_creators=agents_creators)
    asyncio.run(run_demo_loop(agent_manager, model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH))

   