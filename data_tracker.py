import matplotlib.pyplot as plt
import csv
import os
import sys
import getopt


helptext = 'data_tracker.py -d data_dir -r -u user -h host -t refreshtime'

try:
    opts, args = getopt.getopt(sys.argv[1:], "d:ru:h:t:", ['dir=', 'remote', 'user=', 'host=', 'time='])
except getopt.GetoptError:
    print helptext
    sys.exit()

tmpdir_name = 'tracker_tmp/'
datadir = 'data/'
remote = False
user = 'petersoj'
host = 'jupiter'
refresh_time = 5

for opt, arg in opts:
    if opt in ('-d', '--dir'):
        datadir = arg
    elif opt in ('-r', '--remote'):
        remote = True
    elif opt in ('-t', '--time'):
        refresh_time = int(arg)
    elif remote:
        if opt in ('-u', '--user'):
            user = arg
        elif opt in ('-h', '--host'):
            host = arg

last_gen_num = -1
maxs = []

textobject = plt.text(10, 100, 'improving?', bbox=dict(facecolor='white', alpha=0.5))

def get_file():
    if remote:
        assert datadir != 'data/'
        os.system('rsync -avzhe ssh ' + user + '@' + host + ':' + datadir + '/data/' + ' ' + tmpdir_name)
        return tmpdir_name + 'stats.ann'
    else:
        return 'data/stats.ann'

def clean():
    if remote:
        os.system('rm -rf ' + tmpdir_name)

def info_text(state):
    color = 'green' if state else 'red' 
    textobject.set_bbox(dict(facecolor=color, alpha=0.5))

plt.ion()
gen_vals = []
plt.xlabel('num generations')
plt.ylabel('max fitness')
while len(gen_vals) < 1:
    with open(get_file(), 'r') as inputfile:
        reader = csv.reader(inputfile)
        reader1 = [x for x in reader][1:]
        gen_vals = [map(int, row) for row in reader1]
    clean()
maxs = [row[2] for row in gen_vals]
last_gen_num = gen_vals[-1][0]
plt.plot(range(last_gen_num + 1), maxs)
plt.axis([0, last_gen_num + 1, 0, 2 * max(maxs)])
plt.draw()
plt.pause(refresh_time)
while True:
    improved_last_check = False
    with open(get_file(), 'r') as inputfile:
        reader = csv.reader(inputfile)
        reader.next()
        gen_vals = [map(int, row) for row in reader]
        if gen_vals[-1][0] > last_gen_num:
            maxs.append(gen_vals[-1][2])
            last_gen_num = gen_vals[-1][0]
            plt.plot(range(last_gen_num + 1), maxs)
            plt.axis([0, last_gen_num + 1, 0, 2 * max(maxs)])
            improved_last_check = True
        plt.draw()
        info_text(improved_last_check)
        plt.pause(refresh_time)
    clean()
