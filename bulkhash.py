import glob
from hashlib import sha512
from optparse import OptionParser

from collector import SampleCollector, UniformCollectorEngine
from flow import HashingFlow
from hasher import HashAndTime
from save_result import Analysis, get_duplications

parser = OptionParser()


def main():
    (options, args) = parser.parse_args()
    files_iter = glob.iglob(pathname='{}/*.{}'.format(options.input, options.extension))

    total_time, dups = 0, 0

    for file_path in files_iter:
        with open(file_path, 'rb') as fbuffer:
            hsf = HashingFlow([
                SampleCollector().use(UniformCollectorEngine, {'blocks': int(options.blocks), 'block_size': 128}),
                HashAndTime(sha512),
                Analysis()
            ])
            total_time = hsf.start({'file': fbuffer})

    with open('analysis-{}-{}-blocks.txt'.format(options.extension, options.blocks), 'w') as f:
        f.write('HASH USING SHA512 FOR {} EXTENSION WITH {} BLOCKS SAMPLED\n'.format(options.extension, options.blocks))
        f.write('TOTAL TIME: {}\n'.format(total_time))
        f.write('TOTAL DUPLICATIONS: {}\n'.format(get_duplications()))


if __name__ == '__main__':
    parser.add_option('-e', '--extension', help='select an extension to calculate hash')
    parser.add_option('-i', '--input', help='select directory of dataset')
    parser.add_option('-b', '--blocks', help='number of blocks to sample')
    parser.add_option('-o', '--output', help='location for the output analysis')
    main()
