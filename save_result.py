from flow import FlowStep
import gc

total_time = 0
hash_values = []
duplications = 0

class Analysis(FlowStep):
    def prepare(self, prev_output):
        self.last_hash, self.last_hash_time = prev_output

    def exec(self):
        global total_time, hash_values, duplications
        total_time += self.last_hash_time
        if self.last_hash not in hash_values:
            hash_values.append(self.last_hash)
        else:
            duplications += 1

    def finish(self):
        global total_time, duplications
        del self.last_hash_time
        del self.last_hash
        gc.collect()
        return total_time, duplications
