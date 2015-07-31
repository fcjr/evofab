from gui_ann_runner import GuiAnnRunner
from grid import Grid
import ann_io
import sys
import getopt
import sys

helptext = 'loopCurrentBest.py -A annfile -W worldfile'

try:
    opts, args = getopt.getopt(sys.argv[1:], "A:W:", ["ANNfile=", "Worldfile="])
except getopt.GetoptError:
    print helptext
    sys.exit()

ann_file = None
world_file = None

for opt, arg in opts:
    if opt in ('-A', '--ANNfile'):
        ann_file = arg
    elif opt in ('-W', '--Worldfile'):
        world_file = arg

while(True):
	n = ann_io.load(ann_file)
	ideal_grid = Grid(scale=50, path=world_file)
	runner = GuiAnnRunner(ideal_grid)
	runner.run(n, iterations=1000)
