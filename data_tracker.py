import matplotlib.pyplot as plt
import csv
import os
import sys


tmpdir_name = 'tracker_tmp/'

last_gen_num = -1
maxs = []

remote = False
remote_dir = None
if sys.argv[1] == '-r':
    remote_dir = sys.argv[2]
    remote = True

def get_file():
    print 'getting'
    if remote:
        assert remote_dir != None
        os.system('rsync -avzhe ssh petersoj@jupiter.union.edu:' + remote_dir + 'data/' + ' ' + tmpdir_name)
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
