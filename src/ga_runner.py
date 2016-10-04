from ann_genetic_algorithms import AnnPopulation
from phys_printer_genetic_algorithms import PhysPopulation
from grid import Grid
import datetime
import getopt
import sys
import os
import errno

helptext = 'ga_runner.py -v -d -t threadnum -o outputfolder -p serial_port -s sensor_port'

try:
    opts, args = getopt.getopt(sys.argv[1:], "vdt:o:p:s:k:z:c:", ["visual", "dumping", "threadnum=", "outputfolder=", "port=", "sensor_port=", "conveyor_port=", "z_port=", "camera=",]) 
except getopt.GetoptError:
    print helptext
    sys.exit()

is_visual = False
is_dumping = False
num_threads = 5
outputfolder = 'data/'
port = ''
sensor_port = ''
conveyor_port = ''
z_port = ''
camera = 0

for opt, arg in opts:
    if opt in ('-v', '--visual'):
        is_visual = True
    elif opt in ('-d', '--dumping'):
        is_dumping = True
    elif opt in ('-t', '--threadnum'):
        num_threads = int(arg)
    elif opt in ('-o', '--outputfolder'):
        outputfolder = arg
    elif opt in ('-p', '--port'):
        port = arg.strip()
    elif opt in ('-s', '--sensor_port'):
        sensor_port = arg.strip()
    elif opt in ('-k', '--conveyor_port'):
        conveyor_port = arg.strip()
    elif opt in ('-z', '--z_port'):
        z_port = arg.strip()
    elif opt in ('-c', '--camera'):
        camera = int(arg)

current_time = datetime.datetime.now()

param = {
        'pop_size' : 80,
        'mutation_rate' : 0.15,
        'mutation_range' : (-30, 30),
        'cull_num' : 56,
        'ann_input' : 9,
        'ann_hidden' : 26,
        'ann_output' : 4,
        'cell_scale' : 30,
        'inputs' : ['worlds/v_big.test'],
        'random_seed' : int(current_time.strftime('%s')),
        'time' : current_time,
        'num_gens' : 8000,
        'printer_runtime' : 500,
        'units_per_cell' : 10,
        'reward_for_correct' : 100,
        'punishment_for_incorrect': 30,
        'crossover_rate': .5,
        'recur_mode': 3,
        'time_to_recur': 2
        }

if is_dumping:
    outputfolder = outputfolder.strip()
    if outputfolder[-1] != "/":
        outputfolder = outputfolder + "/"
    if not os.path.isdir(outputfolder):
        try:
            os.makedirs(outputfolder)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
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

if port:
    population = PhysPopulation(
            param['random_seed'],
            param['printer_runtime'],
            param['pop_size'],
            param['mutation_rate'],
            param['mutation_range'],
            param['crossover_rate'],
            param['cull_num'],
            param['ann_input'],
            param['ann_hidden'],
            param['ann_output'],
            port,
            sensor_port,
            conveyor_port,
            z_port,
            camera,
            outputfolder=outputfolder,
            is_visual=is_visual,
            dump_to_files=is_dumping,
            )
else:
    population = AnnPopulation(
            param['random_seed'],
            param['printer_runtime'],
            param['pop_size'],
            param['mutation_rate'],
            param['mutation_range'],
            param['crossover_rate'],
            param['cull_num'],
            param['ann_input'],
            param['ann_hidden'],
            param['ann_output'],
            outputfolder=outputfolder,
            reward_for_correct=param['reward_for_correct'],
            punishment_for_incorrect=param['punishment_for_incorrect'],
            goal=param['inputs'],
            is_visual=is_visual,
            dump_to_files=is_dumping,
            cell_size = param['cell_scale'],
            units_per_cell=param['units_per_cell'],
            recur = param['recur_mode'],
            )
population.iterate(param['num_gens'], num_threads)
