import matplotlib.pyplot as plt
import csv
import os
import sys
import getopt


helptext = 'data_tracker.py -d data_dir -r -u user -h host'

try:
    opts, args = getopt.getopt(sys.argv[1:], "d:ru:h::", ['dir=', 'remote', 'user=', 'host='])
except getopt.GetoptError:
    print helptext

tmpdir_name = 'tracker_tmp/'
datadir = 'data/'
remote = False
user = 'petersoj'
host = 'jupiter'

for opt, arg in opts:
    if opt in ('-d', '--dir'):
        datadir = arg
    elif opt in ('-r', '--remote'):
        remote = True
    elif remote:
        if opt in ('-u', '--user'):
            user = arg
        elif opt in ('-h', '--host'):
            host = arg

last_gen_num = -1
maxs = []

def get_file():
    print 'getting'
    if remote:
        assert datadir != 'data/'
        os.system('rsync -avzhe ssh ' + user + '@' + host + ':' + datadir + '/data/' + ' ' + tmpdir_name)
        return tmpdir_name + 'stats.csv'
    else:
        return 'data/stats.csv'

def clean():
    if remote:
        os.system('rm -rf ' + tmpdir_name)

plt.ion()
gen_vals = []
while len(gen_vals) < 1:
    with open(get_file(), 'r') as inputfile:
        reader = csv.reader(inputfile)
        reader1 = [x for x in reader][1:]
        print reader1
        gen_vals = [map(int, row) for row in reader1]
    clean()
maxs = [row[2] for row in gen_vals]
last_gen_num = gen_vals[-1][0]
plt.plot(range(last_gen_num + 1), maxs)
plt.axis([0, last_gen_num + 1, 0, 5 * max(maxs)])
plt.draw()
plt.pause(0.05)
while True:
    with open(get_file(), 'r') as inputfile:
        reader = csv.reader(inputfile)
        reader.next()
        gen_vals = [map(int, row) for row in reader]
        if gen_vals[-1][0] > last_gen_num:
            maxs.append(gen_vals[-1][2])
            last_gen_num = gen_vals[-1][0]
            plt.plot(range(last_gen_num + 1), maxs)
            plt.axis([0, last_gen_num + 1, 0, 5 * max(maxs)])
        plt.draw()
        plt.pause(0.05)
    clean()
