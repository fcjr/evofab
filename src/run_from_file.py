from ann_runner import AnnRunner
from grid import Grid
import ann_io

n = ann_io.load('outputfile')
ideal_grid = Grid(scale=60, path='corner.test')
runner = AnnRunner(ideal_grid)
runner.run(n)
