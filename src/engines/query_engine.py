#import sys, os
#sys.path.append('/home/davi/Desktop/MonkAI_agent')
import os
from openai import AzureOpenAI
from openai.types.chat import ChatCompletion
import config

# import config
from typing import List, Dict

import langchain
from langchain.vectorstores import faiss
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_openai.chat_models import AzureChatOpenAI
import re
import json
from dataclasses import dataclass, asdict


@dataclass
class OpenAIMessage:
    """
    Representa uma mensagem trocada entre o usuário e o assistente.
    """

    role: str
    """Indicates the role of the message sender (user or assistant)."""
    content: str
    """The content of the message."""

    def asdict(self):
        """
        Converte a instância em um dicionário.

        Returns:
            dict: Um dicionário representando a instância.
        """
        return asdict(self)

class QueryEngine:
    """
    Handles interactions with the OpenAI API for using the GPT model.
    """

    def __init__(self, seed=42):
        """Initializes a QueryEngine object.

        Args:
            seed (int, optional): The random seed to use. Defaults to 42.
        """
        self.model = config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH

        self.temperature = 0
        self.seed = seed
        self.max_tokens = 1000

        self.client = AzureOpenAI(
            api_key=config.OPENAI_API_KEY_BRASILSOUTH,
            # api_version = "2023-05-15",
            api_version=config.GPT4o_OPENAI_API_VERSION_BRASILSOUTH,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
        )

        self.gpt4oclient = AzureOpenAI(
            api_key=config.OPENAI_API_KEY_BRASILSOUTH,
            # api_version = "2023-05-15",
            api_version=config.GPT4o_OPENAI_API_VERSION_BRASILSOUTH,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
        )

        self.embedding = AzureOpenAIEmbeddings(
            openai_api_key=config.OPENAI_API_KEY,
            # openai_api_base=config.OPENAI_AZURE_ENDPOINT,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT,
            openai_api_version=config.OPENAI_API_VERSION,
            deployment="text-embedding-ada-002",
            model=config.OEPENAI_EMBEDDING_MODEL,
            chunk_size=1,
            embedding_ctx_length=4096,
        )

    def run_classify(self, text, descricao=""):
        """
        Runs a query on the OpenAI API to classify questions.

        Args:
            text (str): The text to find synonyms for.
            descricao (str, optional): Enummerate the classification needed. 
                                    
        Returns:
            The response from the OpenAI API.
        """

        messages = [
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "Você é um assistente de classe mundial que classifica perguntas. E retorna apenas o número relacionado à classificação."
            }
        ]
        },
        {
        "role": "assistant",
        "content": [
            {
            "type": "text",
            "text": '''Não faça suposições sobre quais valores inserir nas funções. Peça esclarecimentos se uma solicitação do usuário for ambígua.
            
            Selecione a classificação da pergunta com base na descrição a seguir:
            
            **Categorias de Perguntas**:
              1. **Perguntas relacionadas sobre resumo vivoflow**: Solucitaçao esplisita do resuma ou reporte de vivoflow. Precisa conter as palavra resumo ou reporte.\n            
              Exemplo:
                - **Pergunta**: Enviar o resumo do vivoflow
                - **Resposta**: 1
                            
              2. **Perguntas relacionadas ao status de um pedido especificado pelo ID**:  Estas perguntas solicitam o status de um pedido e devem conter um número de pedido com exatamente 7 dígitos na pergunta.
              Exemplo:  
                - **Pergunta**: Qual o status do pedido 1234567?
                - **Resposta**: 2
                                      
              3. **Outras perguntas**: Qualquer pergunta que não se enquadre nas categorias anteriores (1 e 2) deve ser classificada como ativar função SQL.
              Exemplo:
                - **Pergunta**: Como posso conectar ao banco de dados?
                - **Resposta**: 3
                **Exemplo Completo**:<Question> Enviar o resumo do vivoflow </Question>
                                     <Answer> 1 </Answer>

                                     <Question> reporte do vivoflow </Question>
                                     <Answer> 1 </Answer>
                                                     
                                     <Question> Qual o status do pedido 1234567? </Question>
                                     <Answer> 2 </Answer>  

                                     <Question> Pode me dar o status do pedido 1264867? </Question>
                                     <Answer> 2 </Answer>              
                                     
                                     <Question> Quantidades de pedido de vivoflows? </Question>                
                                     <Answer> 3 </Answer>'''
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"{text}"
            }
        ]
        }
    ]
        
        

        query_response = self.client.chat.completions.create(
            model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,
            messages=messages,
            temperature=0,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response

    def run_query(
        self, text, tools=None, prev_messages: List[OpenAIMessage] = [], tools_choice=None, system_message=None
    ) -> ChatCompletion:
        """Runs a query on the OpenAI API.

        Args:
            text (str): The text of the query.
            tools (Optional[List[str]], optional): The list of tools to use. Defaults to None.
            prev_messages (List[OpenAIMessage], optional): The previous messages in the conversation. Defaults to [].

        Returns:
            ChatCompletion: The response from the OpenAI API.
        """

        messages = system_message
        if system_message is None:
            messages = [
                {
                    "role": "system",
                    "content": "Você é um assistente de classe mundial, treinado para ajudar executivos, fornecendo-lhes informações precisas.",
                }
            ]
        messages = messages + [m.asdict() for m in prev_messages]
        messages.append({"role": "user", "content": text})

        if tools:
            return self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                seed=self.seed,
                max_tokens=self.max_tokens,
                tools=tools,
                tool_choice=tools_choice
            )
        else:
            return self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                seed=self.seed,
                max_tokens=self.max_tokens,
            )

    def run_synonym_query(self, text, descricao=""):
        """Runs a query on the OpenAI API to find synonyms.

        Args:
            text (str): The text to find synonyms for.

        Returns:
            The response from the OpenAI API.
        """
        
        messages = [
            {
                "role": "system",
                "content": "Você é um assistente de classe mundial que reescreve mensagens de texto (i.e. mensagens de chat) para que pareçam mais profissionais.",
            },
            {
                "role": "user",
                "content": f"Reescreva a mensagem seguinte, mas mantenha a mensagem curta e sem perder o sentido. Elimine qualquer redundância de informação. Não use o nome do usuário na resposta. Mantenha as quebras de linhas. {descricao}",
            },
            {"role": "user", "content": text},
        ]

        query_response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response

    def run_rag_query(self, question, context):
        """Runs a RAG query

        Args:
            question (str): main question used in the query
            context (str): additional context for the query

        Returns:
            The response from the OpenAI API.
        """

        messages = [
            {
                "role": "system",
                "content": "Você é um assistente com 30 anos de experiencia para responder perguntas de negócios com base num contexto.",
            },
            {
                "role": "user",
                "content": f"Dado o contexto abaixo, responda a pergunta\n\nContexto: {context}, Pergunta: {question}:",
            },
        ]
        query_response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response

    def run_nl2sql_query(self, query, sql_description, prev_messages = [OpenAIMessage], rules= None):
        """
        Function that runs a query to convert natural language to sql

        Args: 
            query (str): query being made
            sql_description (str): description of the sql table that will be consulted
            prev_messages (OpenAIMessage): previous queries taht were made, added for context
            rules (str): additional rules that might optionally be used for context

        Returns the query response
        """
        prompt = f"""
                Dado a descricao das tabelas SQL a seguir, escreva consultas com base na solicitação do usuário. Os sininimos fornecidos podem ser usados (CASO SEJA PRECISO) para interpretar a solicitação do usuario. \n
                DESCRICAO: {sql_description}\n
                SOLICITACAO ANTERIOR: {" | ".join([str(m.asdict()) for m in prev_messages])}\n
                SOLICITACAO ATUAL: {query}:\n\n
                Utilice as siguentes definições, só se o usuario mensina no  mensage, para auxilirse a entender a solicitação:\n
                {''.join(rules)}
                Retorne uma string SQL executavel.
            """
        
        #query_response = self.client.completions.create(
        query_response = self.client.completions.create(
            model=config.OPENAI_GPT_MODEL_INSTRUCT,
            prompt=prompt,
            temperature=0.2,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response

    #def _remove_special_characters(self,text):
    #    pattern = r'[^a-zA-Z0-9\s]'
    #    cleaned_text = re.sub(pattern, '', text)
    #    return cleaned_text


    def run_nl2sql_query2(self, query, sql_description, prev_messages = [], rules= None):
        """
        Function that runs a query to convert natural language to sql, similar to the previous function except it uses
        a different model and adds extra details for generating the sql in text

        Args: 
            query (str): query being made
            sql_description (str): description of the sql table that will be consulted
            prev_messages (OpenAIMessage): previous queries taht were made, added for context
            rules (str): additional rules that might optionally be used for context

        Returns the query response
        """

        prompt = [{
                    "role":"system",
                  "content":"Você é um asistente virtual para escrever código em SQL, apenas o código para ser executado. Não é necessário criar a tabela."             
                 },
               {"role":"assistant" ,
                   "content": f"""
                Dado a descricao das tabelas SQL a seguir, escreva consultas com base na solicitação do usuário.
                Certifique-se de que as consultas usem COUNT apenas em colunas que não sejam de text (como números inteiros ou datas)
                para evitar erros. Por exemplo, se eu tiver uma tabela com colunas: id (int), nome (text) e create_at (data), uma consulta válida seria SELECT COUNT(id) FROM my_table
                   \n
                {sql_description}\n
                SOLICITACAO ANTERIOR: {" | ".join([json.dumps(m.asdict()) for m in prev_messages])}\n
                Retorne uma string SQL executavel.
            """},
           {"role":"assistant",
                  "content":"""Qualquer bloco de código SQL sempre colocar entre ``` 

                            Exemplo: ```SELECT COUNT(VENDAS)
                                        FROM vendas```
                            """},
                {"role":"user",
                  "content":query.lower()}
                ]
        if rules is not None:
              prompt.append({"role": "assistant",
                   "content":f"Utilize as siguentes definições, só se o usuario menciona no  mensage, para auxiliar e entender a solicitação: {' '.join(rules)}"
              })
      
        #query_response = self.client.completions.create(
        query_response = self.client.chat.completions.create(
            model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,
            messages=prompt,
            temperature=0.2,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response
    
    def run_nl2azuresql_query(self, query, sql_description, prev_messages = [], rules= None):
        """
        Function that runs a query to convert natural language to sql, similar to the previous function except it uses
        a different model and adds extra details for generating the sql in text

        Args: 
            query (str): query being made
            sql_description (str): description of the sql table that will be consulted
            prev_messages (OpenAIMessage): previous queries taht were made, added for context
            rules (str): additional rules that might optionally be used for context

        Returns the query response
        """

        prompt = [{
                    "role":"system",
                  "content":"Você é um asistente virtual para escrever código em SQL para Azure SQL serverless, apenas o código para ser executado. Não é necessário criar a tabela."             
                 },
               {"role":"assistant" ,
                   "content": f"""
                Dado a descricao das tabelas SQL a seguir, escreva consultas com base na solicitação do usuário.
                Certifique-se de que as consultas usem COUNT apenas em colunas que não sejam de text (como números inteiros ou datas)
                para evitar erros. Por exemplo, se eu tiver uma tabela com colunas: id (int), nome (text) e create_at (data), uma consulta válida seria SELECT COUNT(id) FROM my_table.
                Certifique que todo query tenha campos de saída usando AS, por exemplo se o query é 'SELECT pedidos FROM table' 
                crie 'SELECT pedidos FROM table AS pedidos'.
                   \n
                {sql_description}\n
                SOLICITACAO ANTERIOR: {" | ".join([json.dumps(m.asdict()) for m in prev_messages])}\n
                Retorne uma string SQL executavel.
            """},
           {"role":"assistant",
                  "content":"""Qualquer bloco de código SQL sempre colocar entre ``` 

                            Exemplo: ```SELECT COUNT(VENDAS)
                                        FROM vendas```
                            """},
                {"role":"user",
                  "content":query.lower()}
                ]
        if rules is not None:
              prompt.append({"role": "assistant",
                   "content":f"Utilize as siguentes definições, só se o usuario menciona no  mensage, para auxiliar e entender a solicitação: {' '.join(rules)}"
              })
      
        #query_response = self.client.completions.create(
        query_response = self.client.chat.completions.create(
            model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,
            messages=prompt,
            temperature=0.2,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response
    
    


    def attempt_sql_fix(self, sql_string: str, error_string: str) -> str:
        """
        Function that runs an openAi query to correct any sql strings that might return errors.

        Args: 
            sql_string (str): sql that was executed
            error_string (str): error raised

        Returns the query response with the corrected sql
        """
        prompt =[{
                    "role":"system",
                  "content":"Você é um asistente virtual para corregir código em SQL, apenas o código para ser executado. Não é necessário criar a tabela."             
                 },
              {"role":"assistant",
                  "content":""" Qualquer bloco de código SQL sempre colocar entre ``` 

                            Exemplo: ```SELECT COUNT(VENDAS)
                                        FROM vendas```
                            """},
                {"role": "user", "content": f"""Dado a string SQL e o erro abaixo, escreva uma nova string SQL que consiga corrigir o erro.
                SQL: {sql_string}\n
                ERRO: {error_string}:\n\n
                Retorne uma string SQL executavel."""}]
        
        # query_response = self.client.chat.completions.create(
        query_response = self.client.chat.completions.create(
            model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,
            messages=prompt,
            #prompt=prompt,
            temperature=0.2,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response
    
    def attempt_azuresql_fix(self, sql_string: str, error_string: str) -> str:
        """
        Function that runs an openAi query to correct any sql strings that might return errors.

        Args: 
            sql_string (str): sql that was executed
            error_string (str): error raised

        Returns the query response with the corrected sql
        """
        prompt =[{
                    "role":"system",
                  "content":"Você é um asistente virtual para corregir código em SQL para Azure SQL serverless, apenas o código para ser executado. Não é necessário criar a tabela."             
                 },
              {"role":"assistant",
                  "content":"""Quando tentando usar COUNT em colunas com valor do tipo 'text' use a função CAST para converter os dados para um tipo de dado compatível,
                  por exemplo quando corrigindo 'SELECT COUNT(ID_PEDIDO) FROM vivoflow' faça 'SELECT COUNT(CAST(ID_PEDIDO AS VARCHAR(MAX))) FROM vivoflow'.  
                  Qualquer bloco de código SQL sempre colocar entre ``` 

                            Exemplo: ```SELECT COUNT(VENDAS)
                                        FROM vendas```
                            """},
                {"role": "user", "content": f"""Dado a string SQL e o erro abaixo, escreva uma nova string SQL que consiga corrigir o erro.
                SQL: {sql_string}\n
                ERRO: {error_string}:\n\n
                Retorne uma string SQL executavel."""}]
        
        # query_response = self.client.chat.completions.create(
        query_response = self.client.chat.completions.create(
            model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,
            messages=prompt,
            #prompt=prompt,
            temperature=0.2,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response
    
    def pipeline_tb(self,text):
        """
        Function that runs an openAI query to extract a dataset table from another string

        Args:
            text (str): full string

        Returns:
            result (str): the name of a dataset table
        """

       
        
        prompt =[{
                    "role":"system",
                  "content":"Você é um assistente virtual especializado em extrair apenas o nome da tabela. e.g. Question: gerar a pizza dos alunos da tabela participantes. Tabela: participantes, Extraia apenas o nome da tabela "             
                 },
                {"role": "user", "content": f"Question: {text}."}]
        
        result = self.client.chat.completions.create(
            model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,
            messages=prompt,
            temperature=1,
            seed=self.seed,
            max_tokens=self.max_tokens
        )
        
        return result

    def run_nl2mongo_query(self, query, sql_description, prev_messages = [], rules= None):
        prompt = [{
                    "role":"system",
                  "content":"Você é um asistente virtual para escrever pipline para executar na função aggregate em PyMongo para base de dados Azure CosmoDB."             
                 },
               {"role":"assistant" ,
                   "content": f"""
                Dado a descricao das tabelas  a seguir, escreva uma pipline de consulta que responda a solicitação do usuário, e seleciona a tabela sobre a que inicia a consulta.\n
                {sql_description}\n
                SOLICITACAO ANTERIOR: {" | ".join([json.dumps(m.asdict()) for m in prev_messages])}\n
                Retorne uma string MongoDb.
            """},
           {"role":"assistant",
                  "content":"""Qualquer bloco de código do pipline sempre colocar entre ``` e o nome da tabela sempre colocar entre <>. Não usar comentarios no código do pipeline. 
                            IMPORTANTE: Tem em conta que o piplein é para Azure cosmoDB, por isso:
                             1. Não usar funções que não sejam suportadas por Azure CosmoDB. 
                             2. Não usar as funções '$project' ou '$match' depois de ter usado a função '$sort'.
                            
                                
                            Exemplo:
                             USER: Liste vendas concluidas
                             ASISTENTE: tabela <vendas>  pipeline ```[{"$match": {"status": "A"}}]```

                            Exemplo:
                             USER: Estado do serviço com id B
                             ASISTENTE: tabela <servicos>  pipeline
                               ``` [
                                        {
                                            "$match": {
                                                "ID_SERVICO": id_servico  # Filter by the service ID
                                            }
                                        },
                                        {
                                            "$project": {
                                                "_id": 0,  # Exclude the _id field
                                                "estado_servico": 1  # Include only the estado_servico field
                                            }
                                        }
                                    ]```
                            """},
                {"role":"user",
                  "content":query}
                ]
        if rules is not None:
              prompt.append({"role": "assistant",
                   "content":f"Utilize as siguentes definições, só se o usuario menciona no  mensage, para auxiliar e entender a solicitação: {' '.join(rules)}"
              })
      
        #query_response = self.client.completions.create(
        query_response = self.client.chat.completions.create(
            model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,
            messages=prompt,
            temperature=0.2,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response
    
    def attempt_mongo_fix(self, sql_string: str, error_string: str) -> str:
        

        prompt =[{
                    "role":"system",
                  "content":"Você é um asistente virtual para corregir os pipeline para executar na função aggregate em PyMongo, apenas o código para ser executado em base de dados Azure CosmoDB."             
                 },
              {"role":"assistant",
                  "content":"""Qualquer bloco de código do pipline sempre colocar entre ```. Não usar comentarios no código do pipeline.
                                IMPORTANTE: Tem em conta que o piplein é para Azure cosmoDB, por isso:
                                    1. Não usar funções que não sejam suportadas por Azure CosmoDB. 
                                    2. Não usar as funções '$project' ou '$match' depois de ter usado a função '$sort'.

                            Exemplo:
                             ASISTENTE: tabela <vendas>  pipeline ```[{"$match": {"status": "A"}}]```
                             
                            Exemplo:
                                ASISTENTE: tabela <servicos>  pipeline
                               ``` [
                                        {
                                            "$match": {
                                                "ID_SERVICO": id_servico  # Filter by the service ID
                                            }
                                        },
                                        {
                                            "$project": {
                                                "_id": 0,  # Exclude the _id field
                                                "estado_servico": 1  # Include only the estado_servico field
                                            }
                                        }
                                    ]
                            """},
                {"role": "user", "content": f"""Dado a pypline de  mongo e o erro abaixo, escreva uma nova pipline que consiga corrigir o erro, retorne apenas o string MongoDB para ser executado.
                pipeline: {sql_string}\n
                ERRO: {error_string}:\n\n
                Retorne uma pipeline executavel."""}]
        
        # query_response = self.client.chat.completions.create(
        query_response = self.client.chat.completions.create(
            model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,
            messages=prompt,
            #prompt=prompt,
            temperature=0.2,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response

    def verify_sql2nl_query(self, query, sql_description, prev_messages= list[OpenAIMessage], rules= None):
        """
        Function that runs an openAi query to verify if the sql query being made by the user is ambiguous considering
        the structure of the database.

        Args: 
            query (str): query being made
            sql_description (str): description of the sql table that will be consulted
            prev_messages (OpenAIMessage): previous queries taht were made, added for context
            rules (str): additional rules that might optionally be used for context

        Returns the query response with the answer of yes or no to wether te query is ambiguous
        """

        prompt = f"""
                Dada a descrição das tabelas SQL a seguir, verifique se o usuário se refere a uma consulta que pode ser ambígua, ou seja, se o usuário não menciona especificamente a coluna e se refere a um valor que pode estar em duas ou mais colunas de uma tabela. Os sininimos fornecidos podem ser usados (CASO SEJA PRECISO) para interpretar a solicitação do usuario. \n
                DESCRICAO: {sql_description}\n
                SOLICITACAO ANTERIOR: {" | ".join([json.dumps(m.asdict()) for m in prev_messages])}\n
                SOLICITACAO ATUAL: {query}:\n\n"""
        if rules is not None:
            prompt +=  f"""Utilice as siguentes definições, só se o usuario mensina no  mensage, para auxilirse a entender a solicitação:\n
                {''.join(rules)}\n\n"""
        prompt+=  "Retorne Sim ou Nao."
        
        #query_response = self.client.completions.create(
        query_response = self.client.completions.create(
            model=config.OPENAI_GPT_MODEL_INSTRUCT,
            prompt=prompt,
            temperature=0.2,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response


    def run_sql2nl_query(self, query, result):
        """
        Function that runs an openAi query to turn an sql result into a natural language reponse

        Args: 
            query (str): sql query that was made
            result (str): result of the query in sql language

        Returns the openAI reponse containing the natural language answer according to the sql result
        """

        messages = [
            {
                "role": "system",
                "content": """
                    Dado as pergunta e resultado a seguir,
                    seu trabalho é escrever uma mensagem para o usuário descrevendo o resultado.
                    Seja sucinto. 
                    Valores 'None' devem ser substituídos por 'Nenhum'.""",
            },
            {"role": "user", "content": f"Pergunta: {query}\n, Resultado: {result}."},
        ]

        query_response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            seed=self.seed,
            max_tokens=self.max_tokens,
        )

        return query_response
