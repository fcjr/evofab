from ann_genetic_algorithms import AnnPopulation
from grid import Grid
import datetime
import sys

mode = sys.argv[1]
run_type = sys.argv[2]
num_threads = int(sys.argv[3])

is_visual = mode == 'visual'
is_dumping = run_type == 'exp'

param = {
        'pop_size' : 30,
        'mutation_rate' : 0.1,
        'mutation_range' : (-10, 10),
        'cull_num' : 24,
        'ann_input' : 9,
        'ann_hidden' : 8,
        'ann_output' : 4,
        'cell_scale' : 50,
        'inputs' : ['worlds/corner.test', 'worlds/line.test', 'worlds/squiggle.test'],
        'random_seed' : datetime.datetime.now(),
        'num_gens' : 2000,
        'printer_runtime' : 1000,
        'printer_speed' : 900
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
