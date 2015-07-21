from ann import Network
from ann_trainer import AnnTrainer
import ann_io
import sys

ann_extension = '.ann'

outputfile = sys.argv[1]
iterations = int(sys.argv[2])
files = sys.argv[3:]

n = Network(9, 7, 4)
trainer = AnnTrainer()
trainer.train(n, files, iterations)
ann_io.save(n, outputfile + '.ann')
