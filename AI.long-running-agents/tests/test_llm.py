import pytest
from src.core.llm.factory import create_llm_client
from src.core.llm.base import LLMClient

def test_create_anthropic_client():
    client = create_llm_client("anthropic", api_key="test-key")
    assert isinstance(client, LLMClient)

def test_create_openai_client():
    client = create_llm_client("openai", api_key="test-key")
    assert isinstance(client, LLMClient)

def test_invalid_provider():
    with pytest.raises(ValueError):
        create_llm_client("invalid", api_key="test-key")
