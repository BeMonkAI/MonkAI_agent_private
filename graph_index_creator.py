

from llama_index.core import SimpleDirectoryReader
#from llama_index.graph_stores.neo4j import Neo4jPGStore
from llama_index.core import Settings, PropertyGraphIndex, VectorStoreIndex
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor
from monkai_shared.agent.engines.llama_query_engine import LLamaQueryEngine
from monkai_shared.agent.engines.llama_query_engine import AzureRegion
from llama_index.llms.azure_openai import AzureOpenAI
import os

# For Azure OpenAI
api_key = '23177d072ea1454da9867f185e33a934'
azure_endpoint = "https://monkai-openai-northcentralusa.openai.azure.com/"
api_version = '2024-08-01-preview'

llm = AzureOpenAI(
        model="gpt-4o",
        deployment_name='gpt-4o-newversion',
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )

def create_graph_index(directory_path): #, neo4j_uri, neo4j_user, neo4j_password):
    query_engine = LLamaQueryEngine(AzureRegion.NORTHCENTRAL_USA)
    Settings.llm = llm
    Settings.embed_model = query_engine.embedding
    documents = SimpleDirectoryReader(input_files=[os.path.join(directory_path,"IA.txt")]).load_data()
    #graph_store = Neo4jPGStore(neo4j_uri, neo4j_user, neo4j_password)
    index = PropertyGraphIndex.from_documents(
                documents,
                llm=llm,
                embed_model=query_engine.embedding,
                show_progress=True,
                kg_extractors=[
                    SchemaLLMPathExtractor(
                        llm=query_engine.llm
                    )
                ]
                # property_graph_store=graph_store
            )
    #index.property_graph_store.save_networkx_graph(name="./kg.html")
    index.storage_context.persist(persist_dir=os.path.join(directory_path, "storage"))
    return query_engine


def create_vector_index(directory_path): #, neo4j_uri, neo4j_user, neo4j_password):
    query_engine = LLamaQueryEngine()
    Settings.llm = llm
    Settings.embed_model = query_engine.embedding
    documents = SimpleDirectoryReader(directory_path).load_data()
    #graph_store = Neo4jPGStore(neo4j_uri, neo4j_user, neo4j_password)
    index = VectorStoreIndex.from_documents(
                documents,
                llm=llm,
                embed_model=query_engine.embedding,
                show_progress=True,
                # property_graph_store=graph_store
            )
    #index.property_graph_store.save_networkx_graph(name="./kg.html")
    index.storage_context.persist(persist_dir=os.path.join(directory_path, "vstorage"))
    return query_engine



#"/Users/joseangelriveaux/Downloads/Archive (1)/test/"
#NEO4JURI = "bolt://localhost:7687"
#NEO4JUSER = "neo4j"
#NEO4JPASS = "12345678"
directory = "/home/davi/Desktop/MonkAI_agent/documents/examples/example.txt"

create_vector_index(directory)
create_graph_index(directory) #, NEO4JURI, NEO4JUSER, NEO4JPASS)
