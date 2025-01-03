<img src="./assets/mascote_monkai.png" alt="Logo" width="130">

<h2 style="font-family: 'Courier New', monospace; color: green;"> MonkAI_agent</h2>

<h3 style="font-family: 'Courier New', monospace; color: green;"> The simple framework for creating intelligent agents, flows quickly, easily, and customizable.</h3>

<p style="text-align: justify; font-family: Arial, sans-serif; font-size: 16px; color: #555;">
  This is an innovative framework designed to facilitate the creation of intelligent agent flows, offering a simple and customizable approach to the development of autonomous agents.
    
  With this framework, you can create, manage, and optimize agents quickly and efficiently. Whether for specific tasks or more complex applications, it provides a modular base that adapts to your needs. Its simplicity of use, combined with its flexibility, makes it an ideal choice for both beginners and experienced developers.
</p>

<h3 style="font-family: 'Courier New', monospace; color: green;">Install</h3> 

<p style="font-family: Arial, sans-serif; font-size: 16px; color: #555;">
Make sure you have Python 3.11 or higher installed on your system.

Clone this repository:

<pre style="background-color: #f6f8fa; border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
 git clone https://github.com/BeMonkAI/MonkAI_agent.git
</pre>

or

<pre style="background-color: #f6f8fa; border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
pip install MonkAI_agent
</pre>  

Navigate to the project directory and install the dependencies:

<pre style="background-color: #f6f8fa; border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
pip install -r requirements.txt
</pre>

</p>

<h2 style="font-family: 'Courier New', monospace; color: green;">Arquitecture</h2>  

<h3 style="font-family: 'Courier New', monospace; color: green;">1. Main Components</h3>  

<h4 style="font-family: 'Courier New', monospace; color: green;">1.1 Agent creation and management</h4>
<p style="font-family: Arial, sans-serif; font-size: 16px; color: #555;">
The core/ contains the main components where the central logic of the system is located. The base.py contains the definition of the AgentManager class, and the monkai_agent_creator.py contains the definition of the MonkaiAgentCreator class.
  
AgentManager: Manages interaction with agents. Initializes with a client, a list of agent creators, context variables, and streaming and debug options. Has methods to execute conversations asynchronously.

MonkaiAgentCreator: Responsible for creating agent instances. Can be configured to create different types of agents based on the system's needs.
</p>

<h4 style="font-family: 'Courier New', monospace; color: green;"> 1.2 Queries and data processing</h4>

<p style="font-family: Arial, sans-serif; font-size: 16px; color: #555;">
The engines/contain the component responsible for executing specific operations, such as queries and data processing, as well as integration with other models and external systems. The query_engine.py contains the definition of the QueryEngine class.
  
QueryEngine: Main class responsible for performing queries and interacting with the model and other data sources.

</p>

<h3 style="font-family: 'Courier New', monospace; color: green;">2. Interaction Diagram</h3> 
 
<p style="font-family: Arial, sans-serif; font-size: 16px; color: #555;">
The framework's architecture is modular and extensible, allowing the creation and management of AI agents that interact with the user through a query engine. The AgentManager is the central management and orchestration point, coordinating interactions between the user, agents, and query engines.
</p>

<img src="./assets/mascote_monkai.png" alt="Logo" width="130">

<h3 style="font-family: 'Courier New', monospace; color: green;">2.1 Execution Flow</h3>  

<p style="font-family: Arial, sans-serif; font-size: 16px; color: #555;">
a...
b...
c...  

</p>

<h2 style="font-family: 'Courier New', monospace; color: green;">Example</h2>  



