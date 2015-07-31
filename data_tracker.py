import matplotlib.pyplot as plt
import time
import csv

last_gen_num = -1
maxs = []

plt.ion()
with open('data/stats.csv', 'r') as inputfile:
    reader = csv.reader(inputfile)
    reader.next()
    gen_vals = [map(int, row) for row in reader]
    maxs = [row[2] for row in gen_vals]
    last_gen_num = gen_vals[-1][0]
    plt.plot(range(last_gen_num + 1), maxs)
    plt.axis([0, last_gen_num + 1, 0, 5 * max(maxs)])
    plt.draw()
    plt.pause(0.05)
while True:
    with open('data/stats.csv', 'r') as inputfile:
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
