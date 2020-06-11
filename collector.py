import gc
from abc import abstractmethod
from math import ceil
from os import stat as get_stats
from typing import Union

from flow import FlowStep


class SampleCollector(FlowStep):
    def __init__(self):
        self._engine = None

    def use(self, engine, engine_params) -> 'SampleCollector':
        self._engine = engine(**engine_params)
        return self

    @staticmethod
    def _get_metadata(file, metadatas: Union[str, list]):
        m = {
            'mode': 0,
            'ino': 1,
            'dev': 2,
            'nlink': 3,
            'uid': 4,
            'gid': 5,
            'size': 6,
            'atime': 7,
            'mtime': 8,
            'ctime': 9,
        }

        stats = None

        if type(metadatas) is str:
            stats = get_stats(file.name)[m[metadatas]]
        else:
            stats = [get_stats(file.name)[m[meta]] for meta in metadatas]

        return stats

    def prepare(self, prev_output):
        self.file = prev_output['file']

    def exec(self):
        samples = self._engine.collect(self.file, self._get_metadata(self.file, 'size'))
        self.samples = samples

    def finish(self):
        del self.file
        del self._engine
        gc.collect()
        return self.samples


class CollectorEngine:

    @abstractmethod
    def collect(self, file_buffer, file_size):
        pass


class UniformCollectorEngine(CollectorEngine):

    def __init__(self, blocks: int, block_size: int):
        if blocks < 0 or block_size < 10:
            raise Exception('Sampling Size Too Small')

        self.blocks = blocks
        self.size = block_size

    def collect(self, file_buffer, file_size):
        nblocks = ceil(file_size / self.size)
        space = nblocks // (self.blocks + 1)
        curr_block = 0

        samples = []

        while curr_block < nblocks:
            file_buffer.seek(curr_block * self.size, 0)
            buffer = file_buffer.read(self.size)
            samples.append(buffer)
            curr_block += space

        file_buffer.seek((nblocks - 1) * self.size, 0)
        samples.append(file_buffer.read(self.size))

        return samples
