#import sys, os
#sys.path.append('/home/davi/Desktop/MonkAI_agent')
import base64
import logging
from typing import Any
import json
from llama_index.core import Settings
from llama_index.core.base.llms.types import (
    ChatResponse
)
from llama_index.core import   VectorStoreIndex
import config 
from io import BytesIO
from engines.ai_manager import AIManager, AzureRegion

class LLamaQueryEngine:
    def __init__(self, region =  AzureRegion.BRASIL_SOUTH):
        super().__init__()
        self.ai_region_manager:AIManager = AIManager()
        self.llm = self.ai_region_manager.get_gpt_by_region(region)
        self.client = self.llm
        self.illm  =  self.ai_region_manager.get_multimodal_gpt_by_region(region)
        self.embedding = self.ai_region_manager.get_embedding_by_region(region)
        self._id = 0
        Settings.llm = self.llm
        Settings.embed_model = self.embedding
        self.region = region

    def chat(self,messages, region=None, **kwargs: Any):
        if region is None:
            result = self.llm.chat(
                messages=messages,
                **kwargs)
        else:
            logging.info(f"Selecting llm from {region}")
            print(f"Selecting llm from {region}")
            llm = self.ai_region_manager.get_gpt_by_region(region)
            result = llm.chat(
                messages=messages,
                **kwargs)
        
        return result
    
    async def achat(self,messages,region=None, **kwargs: Any):
        #import time
        #id = self._id
        #self._id +=1
        #print(f"Request {id} in time: {time.time()}")
        #if kwargs is None:
       #     kwargs = dict()
        #kwargs["max_retries"] = 0
        #response = None
        #try:
        if region is None:
            response =  await self.llm.achat(
                    messages=messages,
                    **kwargs)
        else:
            logging.info(f"Selecting llm from {region}")
            print(f"Selecting llm from {region}")
            llm =self.ai_region_manager.get_gpt_by_region(region)
            response =  await llm.achat(
                    messages=messages,
                    **kwargs)
       # except Exception as exc:
        #    pass        
        #print(f"Response {id} {response} in time: {time.time()}")
        return response
    
    def retrive_from_tool(self,response:ChatResponse):
        message = response.message
        if 'tool_calls' not in message.additional_kwargs:
            return None
        
        tool_calls = message.additional_kwargs['tool_calls']
        resp = []
        for elem in tool_calls:
            try:
                fun_args = elem.function.arguments
                resp.append(json.loads(fun_args))
            except Exception as ex:
                pass
        return resp
    
    def encode_image(self, image:BytesIO):
        """
        Loads images from a directory and encodes them as base64 strings.

        Args:
            imgsDir (list): List of image file names.
            directory (str): Directory where images are stored.

        Returns:
            list: A list of dictionaries with encoded image URLs.

        Example:
            >>> load_images(['image1.jpg', 'image2.jpg'], '/path/to/images')
            [{'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,...'}}, ...]
        """
        image.seek(0)
        readed = image.read()
        decoded = base64.b64encode(readed).decode('utf-8')
        page = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{decoded}"
            }
        }
        return page
    
    def vector_index(self, documents, region = None):
        if region is None:
            embeding = self.embedding
            llm = self.llm
        else:
            embeding = self.ai_region_manager.get_embedding_by_region(self.region)
            llm = self.ai_region_manager.get_gpt_by_region(self.region)                    
        index = VectorStoreIndex(documents, store_nodes_override=True,embed_model=embeding)
        engine = index.as_chat_engine(similarity_top_k=2, llm=llm) 
        return engine
    
    def complete(self, text:str, region = None):
        if region is None:
            llm = self.llm
        else:
            llm = self.ai_region_manager.get_gpt_by_region(region)
        return llm.complete(text)
    
    def acomplete(self, text:str, region = None):
        if region is None:
            llm = self.llm
        else:
            llm = self.ai_region_manager.get_gpt_by_region(region)
        return llm.acomplete(text)
    
    def icomplete(self, prompt, nodes,  region = None):
        if len(nodes) == 0:
            return None
        
        resps = []
        for i in range(0,len(nodes),10):
            nodes_slice = nodes[i:i+10]
            if region is None:
                llm = self.illm
            else:
                llm = self.ai_region_manager.get_multimodal_gpt_by_region(region)
            resps.append(llm.complete(prompt,nodes_slice))
        if len(resps) > 1:
            prompt = f"""Dado um documento divididos em blocos e o prompt: {prompt}. As siguentes respostas respndem a um mesmo prompt  em diferentes blocos de um mesmo documento. 
                        Seleccione a que melhor responderia a todo o documento das siguentes:

                    """
            for resp in resps:
                prompt += f"    - {resp.text}\n"
            return self.complete(prompt, region)
        return resps[0]
        
    def chat_with_engine(self, engine, prompt, **kwargs):
        return engine.chat(prompt, **kwargs)
    
    #TODO: BaseChatEngine type
    async def achat_with_engine(self, engine, prompt, **kwargs):
        return await engine.complete(prompt, **kwargs)
    
    def modify_prompt(self, prompt, region = None):
        modify_prompt = f'Eres um assistente para ajudar a modificar o texto da siguente mensagem: "{prompt}".'
        return  self.complete(modify_prompt, region)

    async def amodify_prompt(self, prompt,region = None):
        modify_prompt = f'Eres um assistente para ajudar a modificar o texto da siguente mensagem: "{prompt}".'
        return await self.acomplete(modify_prompt, region)

