from .base import LLMClient
from .anthropic import AnthropicClient
from .openai import OpenAIClient

def create_llm_client(provider: str, api_key: str, **kwargs) -> LLMClient:
    if provider == "anthropic":
        return AnthropicClient(api_key=api_key, **kwargs)
    elif provider == "openai":
        return OpenAIClient(api_key=api_key, **kwargs)
    else:
        raise ValueError(f"Unsupported provider: {provider}")
