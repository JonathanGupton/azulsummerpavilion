"""Module containing the MessageQueue base class and implementations"""

from abc import ABC
from abc import abstractmethod
from collections import deque
from typing import Iterable

from azulsummerpavilion.library.actions import Message


class MessageQueue(ABC):
    """Base queue class for messaging events and actions"""

    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def append(self, obj: Message) -> None:
        pass

    @abstractmethod
    def appendleft(self, obj: Message) -> None:
        pass

    @abstractmethod
    def pop(self) -> Message:
        pass

    @abstractmethod
    def popleft(self) -> Message:
        pass

    @abstractmethod
    def extend(self, obj: Iterable[Message]) -> None:
        pass

    @abstractmethod
    def extend_left(self, obj: Iterable[Message]) -> None:
        pass


class MessageDequeue(MessageQueue):
    """Class for storing and processing messages (actions/events)"""

    def __init__(self):
        super().__init__()
        self.queue = deque()

    def __repr__(self):
        return repr(self.queue)

    def __str__(self):
        return str(self.queue)

    def append(self, obj: Message) -> None:
        self.queue.append(obj)

    def appendleft(self, obj: Message) -> None:
        self.queue.appendleft(obj)

    def pop(self) -> Message:
        return self.queue.pop()

    def popleft(self) -> Message:
        return self.queue.popleft()

    def extend(self, objs: Iterable[Message]) -> None:
        self.queue.extend(objs)

    def extend_left(self, objs: Iterable[Message]) -> None:
        self.queue.extendleft(objs)
