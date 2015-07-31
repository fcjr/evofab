from ann_genetic_algorithms import AnnPopulation
from grid import Grid
import datetime
import getopt
import sys

helptext = 'ga_runner.py -v -d -t threadnum -o outputfolder'

try:
    opts, args = getopt.getopt(sys.argv[1:], "vdt:o:", ["visual", "dumping", "threadnum=", "outputfolder="])
except getopt.GetoptError:
    print helptext
    sys.exit()

is_visual = False
is_dumping = False
num_threads = 5
outputfolder = 'data/'

for opt, arg in opts:
    if opt in ('-v', '--visual'):
        is_visual = True
    elif opt in ('-d', '--dumping'):
        is_dumping = True
    elif opt in ('-t', '--threadnum'):
        num_threads = int(arg)
    elif opt in ('-o', '--outputfolder'):
        outputfolder = arg

current_time = datetime.datetime.now()

param = {
        'pop_size' : 400,
        'mutation_rate' : 0.1,
        'mutation_range' : (-10, 10),
        'cull_num' : 320,
        'ann_input' : 9,
        'ann_hidden' : 9,
        'ann_output' : 4,
        'cell_scale' : 50,
        'inputs' : ['worlds/corner.test', 'worlds/line.test', 'worlds/squiggle.test'],
        'random_seed' : int(current_time.strftime('%s')),
        'time' : current_time,
        'num_gens' : 8000,
        'printer_runtime' : 200,
        'printer_speed' : 4050,
        'reward_for_correct' : 20,
        'punishment_for_incorrect': 1,
        }

if is_dumping:
    with open(outputfolder + 'TEST_INFO', 'w') as outputfile:
        for key, val in param.items():
            outputfile.write(key + ' : ' + str(val) + '\n')
        for gridfile in param['inputs']:
            outputfile.write('\n========================\n')
            outputfile.write(gridfile + '\n\n')
            with open(gridfile, 'r') as to_read:
                for line in to_read:
                    outputfile.write(line)
            outputfile.write('\n========================\n')

population = AnnPopulation(
        param['random_seed'],
        param['printer_runtime'],
        param['printer_speed'],
        param['pop_size'],
        param['mutation_rate'],
        param['mutation_range'],
        param['cull_num'],
        param['ann_input'], 
        param['ann_hidden'],
        param['ann_output'],
        param['reward_for_correct'],
        param['punishment_for_incorrect'],
        [Grid(scale=param['cell_scale'], path=val) for val in param['inputs']],
        is_visual=is_visual,
        dump_to_files=is_dumping,
        outputfolder=outputfolder,
        )
population.iterate(param['num_gens'], num_threads)
