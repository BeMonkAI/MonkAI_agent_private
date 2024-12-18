import os
import asyncio
import logging
import re
import secrets  # For secure token generation
import hashlib
import  config
from engines.query_engine import QueryEngine
from .creators.monkai_agent_creator import MonkaiAgentCreator
from .creators.triaggent_agent_creator import TriaggentAgenCreator  # For hashing passwords

# Assuming the following modules have been updated to support async operations
from swarm import Swarm
from swarm.types import Response
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentManager:
    """
    Manages the processing of a PDF document and a Google Sheet, including checking for updates,
    generating briefings, and creating agents for interaction.
    """

    def __init__(self, agents_creators: list[MonkaiAgentCreator], engine:QueryEngine, context_variables=None, stream=False, debug=False):
        """
        Initializes the AgentManager with the provided document link, user path, and user input.

        Args:
            pdf_link (str): The URL link to the PDF document.
            sheet_link (str): The URL link to the Google Sheet.
            user_path (str): The file system path to the user's working directory.
            user_input (str): The user's input or query.
            agent (Agent, optional): The current agent handling the conversation.
            messages (list, optional): The list of previous messages in the conversation.
            context_variables (dict, optional): Context variables for the conversation.
            stream (bool, optional): Whether to stream the response.
            debug (bool, optional): Whether to enable debug mode.
        """
        self.agents_creators = agents_creators
        self.triaggen_agent_criator = TriaggentAgenCreator(agents_creators)
        self.context_variables = context_variables or {}
        self.stream = stream
        self.debug = debug
        self.client = Swarm(client = engine.client)
        self.agent = self.triaggen_agent_criator.get_agent()

    def get_triaggen_agent(self):
        return self.triaggen_agent_criator.get_agent()

    def run(self,user_message:str, user_history:list = None):
        """
        Executes the main workflow:
            - Handles the conversation.

        Returns:
            tuple: A tuple containing the updated messages list and the current agent.
        """
        # Append user's message
        messages=user_history if user_history is not  None else []
        messages=[{"role": "user", "content": user_message}]

        # Run the conversation asynchronously
        response:Response =  self.client.run(
            agent=self.agent,
            model_override=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,
            messages= messages,
            context_variables=self.context_variables,
            stream=self.stream,
            debug=self.debug,
        )
        assert(response is not None)
        return response.messages, response.agent
    
   