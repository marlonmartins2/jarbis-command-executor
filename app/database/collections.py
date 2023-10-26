from enum import Enum


class Collections(str, Enum):
    """
    Enum for collections to be used in database
    Args:
        str (Enum): Enum for collections to be used in database
    """
    COMMANDS = "commands"
    ADVICES = "advices"