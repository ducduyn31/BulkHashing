import gc

import pandas as pd

from flow import FlowStep

total_time = 0
hash_values = []


def get_duplications():
    df = pd.DataFrame(hash_values)
    return len(df[df.duplicated(keep=False)])


class Analysis(FlowStep):
    def prepare(self, prev_output):
        self.last_hash, self.last_hash_time = prev_output

    def exec(self):
        global total_time, hash_values
        total_time += self.last_hash_time
        hash_values.append(self.last_hash)

    def finish(self):
        global total_time
        del self.last_hash_time
        del self.last_hash
        gc.collect()
        return total_time
