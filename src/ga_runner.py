from ann_genetic_algorithms import AnnPopulation
from grid import Grid
import sys

mode = sys.argv[1]
run_type = sys.argv[2]

is_visual = mode == 'visual'
is_dumping = run_type == 'exp'

population = AnnPopulation(300, .1, 60, 9, 8, 4, Grid(scale=50, path='corner.test'), is_visual=is_visual, dump_to_files=is_dumping)
population.iterate(2000, 12)
