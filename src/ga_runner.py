from ann_genetic_algorithms import AnnPopulation
from grid import Grid
import datetime
import getopt
import sys

helptext = 'ga_runner.py -v -d -t threadnum'

try:
    opts, args = getopt.getopt(sys.argv[1:], "vdt:", ["visual", "dumping", "threadnum="])
except getopt.GetoptError:
    print helptext
    assert True == False

is_visual = False
is_dumping = False
num_threads = 5

for opt, arg in opts:
    if opt in ('-v', '--visual'):
        is_visual = True
    elif opt in ('-d', '--dumping'):
        is_dumping = True
    elif opt in ('-t', '--threadnum'):
        num_threads = int(arg)

param = {
        'pop_size' : 10,
        'mutation_rate' : 0.1,
        'mutation_range' : (-10, 10),
        'cull_num' : 8,
        'ann_input' : 9,
        'ann_hidden' : 8,
        'ann_output' : 4,
        'cell_scale' : 50,
        'inputs' : ['worlds/corner.test', 'worlds/line.test', 'worlds/squiggle.test'],
        'random_seed' : datetime.datetime.now(),
        'num_gens' : 2000,
        'printer_runtime' : 300,
        'printer_speed' : 2700
        }

if is_dumping:
    with open('gens/TEST_INFO', 'w') as outputfile:
        for key, val in param.items():
            outputfile.write(key + ' : ' + str(val) + '\n')

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
        [Grid(scale=param['cell_scale'], path=val) for val in param['inputs']],
        is_visual=is_visual,
        dump_to_files=is_dumping,
        )
population.iterate(param['num_gens'], num_threads)
