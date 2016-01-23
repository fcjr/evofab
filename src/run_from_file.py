from gui_ann_runner import GuiAnnRunner
from grid import Grid
import ann_io
import getopt
import sys

helptext = 'run_from_file.py -A annfile -W worldfile -t time_to_run -u units_per_cell'

try:
    opts, args = getopt.getopt(sys.argv[1:], "A:W:t:u:", ["ANNfile=", "Worldfile=", "time=", "units="])
except getopt.GetoptError:
    print helptext
    sys.exit()

ann_file = None
world_file = None
num_iterations = 1000
units_per_cell = 20

for opt, arg in opts:
    if opt in ('-A', '--ANNfile'):
        ann_file = arg
    elif opt in ('-W', '--Worldfile'):
        world_file = arg
    elif opt in ('-t', '--time'):
        num_iterations = int(arg)
    elif opt in ('-u', '--units_per_cell'):
        units_per_cell = int(arg)

n = ann_io.load(ann_file)
ideal_grid = Grid(scale=30, path=world_file)
runner = GuiAnnRunner(ideal_grid, units_per_cell=units_per_cell)
runner.run(n, iterations=num_iterations)
