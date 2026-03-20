from src.agents.researcher import ResearcherAgent
from src.agents.analyzer import AnalyzerAgent
from src.agents.writer import WriterAgent


class AgentFactory:

    _registry = {}

    @classmethod
    def register_agent(cls, name: str, agent_class):
        """Adds an agent (class) to the registry"""
        cls._registry[name] = agent_class

    @classmethod
    def create(cls, name: str):
        """Creates the new agent class and returns it"""
        if name not in cls._registry:
            raise ValueError(
                f"Agent {name} not registered."
                f"Please provide a suitable agent in this list: {list(cls._registry.keys())}")

        # Takes the class from the dictionary and instatiates it, then it returns the object
        target_class = cls._registry[name]
        return target_class()
    

AgentFactory.register_agent("researcher", ResearcherAgent)
AgentFactory.register_agent("analyzer", AnalyzerAgent)
AgentFactory.register_agent("writer", WriterAgent)




