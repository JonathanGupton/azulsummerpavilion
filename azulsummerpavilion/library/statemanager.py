from azulsummerpavilion.library.components.state import AzulSummerPavilionState
from azulsummerpavilion.library.queue import MessageQueue


class StateManager:
    state: AzulSummerPavilionState
    actions: MessageQueue
    events: MessageQueue
