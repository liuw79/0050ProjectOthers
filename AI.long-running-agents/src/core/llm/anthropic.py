from anthropic import Anthropic
from .base import LLMClient

class AnthropicClient(LLMClient):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def chat(self, messages, **kwargs):
        response = self.client.messages.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.content[0].text

    def chat_stream(self, messages, **kwargs):
        return self.client.messages.stream(
            model=self.model,
            messages=messages,
            **kwargs
        )
