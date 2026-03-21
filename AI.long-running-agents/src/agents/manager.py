from src.agents.base import Agent
from src.agents.initializer import InitializerAgent
from src.agents.coder import CodingAgent

class AgentManager:
    def __init__(self, config):
        self.config = config

    def create_initializer(self) -> InitializerAgent:
        """创建初始化代理"""
        return InitializerAgent(self.config)

    def create_coder(self) -> CodingAgent:
        """创建编码代理"""
        return CodingAgent(self.config)

    def run_session(self, agent: Agent) -> dict:
        """运行代理会话"""
        return agent.run()
