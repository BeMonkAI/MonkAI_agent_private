from enum import Enum

class ProviderEnum(Enum):
    """
    Enum for providers
    """
    OPENAI = "openai"
    ANTHROPIC="anthropic"
    AZURE="azure"
    GOOGLE="google"
    AWS="aws"
    GROQ="groq"
    MISTRAL="mistral"
    OLLAMA="ollama"
    HUGGINGFACE="huggingface"
    SAMBANOVA="sambanova"
    WATSONX="watsonx"

    