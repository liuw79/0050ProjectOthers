from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    def run(self) -> dict:
        """运行代理并返回结果"""
        pass
