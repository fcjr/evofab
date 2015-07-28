from gui_ann_runner import GuiAnnRunner
from grid import Grid
import ann_io
import sys

ann_file = sys.argv[1]
world_file = sys.argv[2]

n = ann_io.load(ann_file)
ideal_grid = Grid(scale=50, path=world_file)
runner = GuiAnnRunner(ideal_grid)
runner.run(n, iterations=1000, x=325, y=125)
