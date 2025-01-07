
from enum import Enum
import logging 
import config
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.multi_modal_llms.azure_openai import AzureOpenAIMultiModal


class AzureRegion(Enum):
    BRASIL_SOUTH = "br_south"
    EAST_USA = "east_uas"
    EAST_USA2 = "east_usa2"
    WEST_USA = "weast_usa"
    NORTHCENTRAL_USA = "northcentral_usa"

class AIManager:
    """Gerenciador de instâncias de modelos de IA para diferentes regiões do Azure."""
    
    def __new__(cls) -> None:
        """
        Cria uma nova instância da classe AIManager, garantindo que apenas uma instância exista (Singleton).

        Returns:
            AIManager: A instância única da classe AIManager, ou None em caso de erro na inicialização.
        """
        if not hasattr(cls, '_instance'):
            try:
                cls._instance = super(AIManager, cls).__new__(cls)
                cls._instance._initialize()
            except Exception as ex:
                logging.info(f"ERRO INITIALIZING AIManager {ex}")
                return None
        return cls._instance

    def __create_gpts(self):
        """
        Cria instâncias de modelos GPT para diferentes regiões do Azure e as armazena em um dicionário.

        Returns:
            None
        """
        self.gpt_list = dict()
        self.gpt_list[AzureRegion.BRASIL_SOUTH] = AzureOpenAI(
            model='gpt-4o',
            deployment_name=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,
            api_key=config.OPENAI_API_KEY_BRASILSOUTH,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
            api_version=config.GPT4o_OPENAI_API_VERSION_BRASILSOUTH
            )
        self.gpt_list[AzureRegion.NORTHCENTRAL_USA] = AzureOpenAI(
            model='gpt-4o',
            deployment_name=config.GPT4o_OPENAI_GPT_MODEL_NORTHCENTRALUSA,
            api_key=config.OPENAI_API_KEY_NORTHCENTRALUSA,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_NORTHCENTRALUSA,
            api_version=config.GPT4o_OPENAI_API_VERSION_NORTHCENTRALUSA
            )
        self.gpt_list[AzureRegion.EAST_USA] = AzureOpenAI(
            model='gpt-4o',
            deployment_name=config.GPT4o_OPENAI_GPT_MODEL_EASTUS,
            api_key=config.OPENAI_API_KEY_EASTUS,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_EASTUS,
            api_version=config.GPT4o_OPENAI_API_VERSION_EASTUS
            )
        self.gpt_list[AzureRegion.EAST_USA2] = AzureOpenAI(
            model='gpt-4o',
            deployment_name=config.GPT4o_OPENAI_GPT_MODEL_EASTUS2,
            api_key=config.OPENAI_API_KEY_EASTUS2,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_EASTUS2,
            api_version=config.GPT4o_OPENAI_API_VERSION_EASTUS2
            )
        self.gpt_list[AzureRegion.WEST_USA] = AzureOpenAI(
            model='gpt-4o',
            deployment_name=config.GPT4o_OPENAI_GPT_MODEL_WESTUS,
            api_key=config.OPENAI_API_KEY_WESTUS,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_WESTUS,
            api_version=config.GPT4o_OPENAI_API_VERSION_WESTUS
            )
    
    def __create_embeddings(self):
        """
        Cria instâncias de modelos de embeddings para diferentes regiões do Azure e as armazena em um dicionário.

        Returns:
            None
        """
        self.embeddings_list = dict()
        self.embeddings_list[AzureRegion.BRASIL_SOUTH] = AzureOpenAIEmbedding(
            model=config.OEPENAI_EMBEDDING_MODEL_BRASILSOUTH,
            deployment_name=config.OEPENAI_EMBEDDING_MODEL_NAME_BRASILSOUTH,
            api_key=config.OPENAI_API_KEY_BRASILSOUTH,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
            api_version=config.GPT4o_OPENAI_API_VERSION_BRASILSOUTH
            )
        self.embeddings_list[AzureRegion.NORTHCENTRAL_USA] = AzureOpenAIEmbedding(
            model=config.OEPENAI_EMBEDDING_MODEL_NORTHCENTRALUSA,
            deployment_name=config.OEPENAI_EMBEDDING_MODEL_NAME_NORTHCENTRALUSA,
            api_key=config.OPENAI_API_KEY_NORTHCENTRALUSA,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_NORTHCENTRALUSA,
            api_version=config.GPT4o_OPENAI_API_VERSION_NORTHCENTRALUSA
            )
        self.embeddings_list[AzureRegion.EAST_USA] = AzureOpenAIEmbedding(
            model=config.OEPENAI_EMBEDDING_MODEL_EASTUS,
            deployment_name=config.OEPENAI_EMBEDDING_MODEL_NAME_EASTUS,
            api_key=config.OPENAI_API_KEY_EASTUS,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_EASTUS,
            api_version=config.GPT4o_OPENAI_API_VERSION_EASTUS
            )
        self.embeddings_list[AzureRegion.EAST_USA2] = AzureOpenAIEmbedding(
            model=config.OEPENAI_EMBEDDING_MODEL_EASTUS2,
            deployment_name=config.OEPENAI_EMBEDDING_MODEL_NAME_EASTUS2,
            api_key=config.OPENAI_API_KEY_EASTUS2,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_EASTUS2,
            api_version=config.GPT4o_OPENAI_API_VERSION_EASTUS2
            )
        self.embeddings_list[AzureRegion.WEST_USA] = AzureOpenAIEmbedding(
            model=config.OEPENAI_EMBEDDING_MODEL_WESTUS,
            deployment_name=config.OEPENAI_EMBEDDING_MODEL_NAME_WESTUS,
            api_key=config.OPENAI_API_KEY_WESTUS,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_WESTUS,
            api_version=config.GPT4o_OPENAI_API_VERSION_WESTUS
            )
        
    def __create_multimodals(self):
        """
        Cria instâncias de modelos multimodais para diferentes regiões do Azure e as armazena em um dicionário.

        Returns:
            None
        """
        self.multimodals_list = dict()
        self.multimodals_list[AzureRegion.BRASIL_SOUTH] = AzureOpenAIMultiModal(
                model="gpt-4o",
                deployment_name=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,
                api_key=config.OPENAI_API_KEY_BRASILSOUTH,
                azure_endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
                api_version=config.GPT4o_OPENAI_API_VERSION_BRASILSOUTH,
               image_detail="high", timeout=60)
        self.multimodals_list[AzureRegion.NORTHCENTRAL_USA] = AzureOpenAIMultiModal(
                model="gpt-4o",
                deployment_name=config.GPT4o_OPENAI_GPT_MODEL_NORTHCENTRALUSA,
                api_key=config.OPENAI_API_KEY_NORTHCENTRALUSA,
                azure_endpoint=config.OPENAI_AZURE_ENDPOINT_NORTHCENTRALUSA,
                api_version=config.GPT4o_OPENAI_API_VERSION_NORTHCENTRALUSA,
               image_detail="high", timeout=60)
        self.multimodals_list[AzureRegion.EAST_USA] = AzureOpenAIMultiModal(
                model="gpt-4o",
                deployment_name=config.GPT4o_OPENAI_GPT_MODEL_EASTUS,
                api_key=config.OPENAI_API_KEY_EASTUS,
                azure_endpoint=config.OPENAI_AZURE_ENDPOINT_EASTUS,
                api_version=config.GPT4o_OPENAI_API_VERSION_EASTUS,
               image_detail="high", timeout=60)
        self.multimodals_list[AzureRegion.EAST_USA2] = AzureOpenAIMultiModal(
                model="gpt-4o",
                deployment_name=config.GPT4o_OPENAI_GPT_MODEL_EASTUS2,
                api_key=config.OPENAI_API_KEY_EASTUS2,
                azure_endpoint=config.OPENAI_AZURE_ENDPOINT_EASTUS2,
                api_version=config.GPT4o_OPENAI_API_VERSION_EASTUS2,
               image_detail="high", timeout=60)
        self.multimodals_list[AzureRegion.WEST_USA] = AzureOpenAIMultiModal(
                model="gpt-4o",
                deployment_name=config.GPT4o_OPENAI_GPT_MODEL_WESTUS,
                api_key=config.OPENAI_API_KEY_WESTUS,
                azure_endpoint=config.OPENAI_AZURE_ENDPOINT_WESTUS,
                api_version=config.GPT4o_OPENAI_API_VERSION_WESTUS,
               image_detail="high", timeout=60)
        
    def _initialize(self):
        """
        Inicializa o AIManager criando instâncias de GPTs, embeddings e multimodais.

        Returns:
            None
        """
        self.__create_gpts()
        self.__create_embeddings()
        self.__create_multimodals()

    def get_gpt_by_region(self, region: AzureRegion):
        """
        Obtém a instância do modelo GPT correspondente à região especificada.

        Args:
            region (AzureRegion): A região para a qual se deseja obter a instância do modelo GPT.

        Returns:
            AzureOpenAI: A instância do modelo GPT correspondente à região.
        """
        return self.gpt_list[region]
    
    def get_embedding_by_region(self, region: AzureRegion):
        """
        Obtém a instância do modelo de embeddings correspondente à região especificada.

        Args:
            region (AzureRegion): A região para a qual se deseja obter a instância do modelo de embeddings.

        Returns:
            AzureOpenAIEmbedding: A instância do modelo de embeddings correspondente à região.
        """
        return self.embeddings_list[region]
    
    def get_multimodal_gpt_by_region(self, region: AzureRegion):
        """
        Obtém a instância do modelo multimodal correspondente à região especificada.

        Args:
            region (AzureRegion): A região para a qual se deseja obter a instância do modelo multimodal.

        Returns:
            AzureOpenAIMultiModal: A instância do modelo multimodal correspondente à região.
        """
        return self.multimodals_list[region]
    
