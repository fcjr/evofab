from ann import Network
from ann_trainer import AnnTrainer
import ann_io
import sys
from os import listdir
from os.path import isfile, join

ann_extension = '.ann'

outputfile = sys.argv[1]
iterations = int(sys.argv[2])
training_dir = sys.argv[3]

files = [ join(training_dir, f) for f in listdir(training_dir) if isfile(join(training_dir, f)) ]

n = Network(9, 7, 4)
trainer = AnnTrainer()
trainer.train(n, files, iterations)
ann_io.save(n, outputfile + '.ann')
