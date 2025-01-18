from azulsummerpavilion.library.queue import MessageQueue
from azulsummerpavilion.library.state import AzulSummerPavilionState


class StateManager:
    state: AzulSummerPavilionState
    actions: MessageQueue
    events: MessageQueue
