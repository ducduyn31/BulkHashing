import time

from flow import FlowStep
import gc


class HashAndTime(FlowStep):
    def __init__(self, alg):
        self.hash = alg()

    def prepare(self, prev_output):
        self.data = prev_output

    def exec(self):
        start_time = time.time()

        for block in self.data:
            self.hash.update(block)

        self.result = self.hash.digest()
        elapsed_time = time.time() - start_time
        self.time = elapsed_time

    def finish(self):
        del self.data
        gc.collect()
        return self.result, self.time
