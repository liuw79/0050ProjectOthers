import pytest
from src.agents.manager import AgentManager
from src.agents.base import Agent

def test_create_initializer():
    manager = AgentManager(config=None)
    initializer = manager.create_initializer()
    assert isinstance(initializer, Agent)

def test_create_coder():
    manager = AgentManager(config=None)
    coder = manager.create_coder()
    assert isinstance(coder, Agent)
