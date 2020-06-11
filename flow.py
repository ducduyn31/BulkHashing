from abc import abstractmethod
from typing import List


class HashingFlow:
    def __init__(self, flow: List['FlowStep']):
        self.flow = flow

    def start(self, init_config):
        prev = init_config

        for step in self.flow:
            step.prepare(prev)
            step.exec()
            prev = step.finish()

        return prev


class FlowStep:

    @abstractmethod
    def prepare(self, prev_output):
        pass

    @abstractmethod
    def exec(self):
        pass

    @abstractmethod
    def finish(self):
        pass
