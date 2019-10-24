from enum import Enum, auto


class OP(Enum):
    QUIT_QUERY = auto()
    OPEN_QUERY = auto()
    PREVIOUS_QUESTION = auto()
    NEXT_QUESTION = auto()
    PAUSE_QUESTION = auto()
    CONTINUE_QUESTION = auto()
    GOTO_QUESTION = auto()
    COMMIT_QUERY = auto()
    PASSIVE_START = auto()
