from gui_ann_runner import GuiAnnRunner
from grid import Grid
import ann_io
import getopt
import sys

helptext = 'run_from_file.py -A annfile -W worldfile -t time_to_run'

try:
    opts, args = getopt.getopt(sys.argv[1:], "A:W:t:", ["ANNfile=", "Worldfile=", "time="])
except getopt.GetoptError:
    print helptext
    sys.exit()

ann_file = None
world_file = None
num_iterations = 1000

for opt, arg in opts:
    if opt in ('-A', '--ANNfile'):
        ann_file = arg
    elif opt in ('-W', '--Worldfile'):
        world_file = arg
    elif opt in ('-t', '--time'):
        num_iterations = int(arg)

n = ann_io.load(ann_file)
ideal_grid = Grid(scale=50, path=world_file)
runner = GuiAnnRunner(ideal_grid)
runner.run(n, iterations=num_iterations)
