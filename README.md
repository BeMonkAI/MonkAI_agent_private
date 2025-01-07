<img src="./assets/mascote_monkai.png" alt="Logo" width="150">


<h2 style="font-family: 'Courier New', monospace; color: green;"> MonkAI_agent</h2>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

<!--or

<pre style="background-color: #f6f8fa; border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
pip install MonkAI_agent
</pre>  -->

Navigate to the project directory and install the dependencies:

<pre style="background-color: #f6f8fa; border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
pip install -r requirements.txt
</pre>

Important* do not forget your configuration file `config.py`, where you save your API Keys.
</p>

<h2 style="font-family: 'Courier New', monospace; color: green;">Arquitecture</h2>  

<h3 style="font-family: 'Courier New', monospace; color: green;">Main Components</h3>  

The `core/` module concentrates on the main components responsible for the central logic of the system. It defines classes and fundamental structures for creating and managing agents and offering security mechanisms.

Definition and Management of Agents: Structures for creating and managing agents are only provided by specialized classes. These classes follow a hierarchy that allows extending and personalizing the behavior of two agents, such as triage and transfer agents.

Security and Validation: A validation decorator protects sensitive functions, verifying whether users can access them. If validation is done, the function is executed; Otherwise, access will be denied with an appropriate message.

The modules' imports and objects are directly related to offering a robust and secure core for the system, focusing on efficient management of agents and protection of its critical functionalities.

<h3 style="font-family: 'Courier New', monospace; color: green;">Practical Module</h3> 

The `examples/` module serves as a repository of practical cases that demonstrate how to use the central components of the system, especially the breeding agents defined in the core module. It presents specific implementations of breeding agents for different tasks, using the breeder agent class as a basis. It constitutes a bridge between the abstract logic of the 'core' and the practical application, allowing users to explore the system's capabilities and adapt the breeding agents to their needs.

Application: The main purpose of this module is to illustrate the flexibility and extensibility of the system, providing practical cases and customization of agents for different scenarios. It guides developers, showing how to create and adapt specialized agents using the `core` structure efficiently, maximizing code reuse, and adding to the defined core architecture.

<h3 style="font-family: 'Courier New', monospace; color: green;">Interaction Diagram</h3> 
 
The framework architecture is modular and extensive, allowing the creation and management of AI agents interacting with the user. The `AgentManager` is the central management and orchestration point, coordinating the interactions between the user and the agents.

<img src="./assets/Arq.png" alt="Logo">

<h4 style="font-family: 'Courier New', monospace; color: green;">Main Classes</h4>  

`AgentManager`: Manages interaction with agents. Initializes with a client, a list of agent creators, context variables, and streaming and debugging options. Has methods to execute conversations asynchronously.

`MonkaiAgentCreator`: This is an abstract class that creates agent instances, returns an Agent object, and provides a brief description of its capabilities. It can be configured to create different types of agents based on the system's needs.

`TriaggentAgentCreator`: Inherits from `MonkaiAgentCreator`, it creates the triage agent that decides which agent should handle the user's request. Based on the instructions provided, it makes functions that transfer the conversation to the appropriate agent. When the selected agent can no longer respond to a given task, the triggering agent is triggered again to choose another agent that better adapts to the needs of the user's request. It provides clear instructions on when to transfer the conversation to each specific agent, a notable difference from this framework. 

<h4 style="font-family: 'Courier New', monospace; color: green;">Agents Examples</h4>   

`PythonDeveloperAgentCreator`: Responsible for creating and managing Python development agents within the system. Provides features related to software development in Python, such as generating code, documenting, testing, and optimizing Python code by generating an executable .py file. Encapsulates the logic needed to create an agent specialized in performing software development tasks in Python to help automate and facilitate the work of Python developers.

`ResearcherAgentCreator`: Responsible for creating and managing research agents within the system. This agent provides features related to information research, such as searching for data, analyzing content, and providing answers based on collected information, and also returns links to the sources consulted. Encapsulates the logic needed to create an agent specialized in performing information research tasks.

`CalculatorAgentCreator`: Responsible for creating and managing calculation agents within the system and providing features related to mathematical operations. Encapsulates the logic needed to make an agent specialized in performing mathematical calculations.

`JournalistAgentCreator`: Created and managed journalism agents within the system. This agent provides functionalities for collecting, analyzing, and summarizing news and articles. It encapsulates the logic required to create an agent specialized in performing journalism tasks, such as reading and summarizing news.

In the `demo.py` file, a demonstration of the multi-agent system is configured and executed, creating all these specialized agents, the Python Developer Agent, the Researcher, the Journalist, and the Calculator, managing them and using a query engine and specific configurations to execute the demonstration asynchronously.


