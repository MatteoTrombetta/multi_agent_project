from enum import Enum, unique

@unique
class Message(Enum):
    HumanMessage: 1
    AIMessage: 2
    ToolMessage: 3
    