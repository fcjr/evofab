from ann_runner import AnnRunner
from grid import Grid
import ann_io
import sys

ann_file = sys.argv[1]
world_file = sys.argv[2]

n = ann_io.load(ann_file)
ideal_grid = Grid(scale=60, path=world_file)
runner = AnnRunner(ideal_grid)
runner.run(n)
