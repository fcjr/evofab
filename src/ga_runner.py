from ann_genetic_algorithms import AnnPopulation
from grid import Grid
import sys

mode = sys.argv[1]
run_type = sys.argv[2]
num_threads = int(sys.argv[3])

is_visual = mode == 'visual'
is_dumping = run_type == 'exp'

population = AnnPopulation(30, .1, 24, 9, 8, 4, [Grid(scale=50, path='worlds/corner.test'), Grid(scale=50, path='worlds/line.test'), Grid(scale=50, path='worlds/squiggle.test')], is_visual=is_visual, dump_to_files=is_dumping)
population.iterate(2000, num_threads)
