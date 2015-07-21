from ann import Network
from ann_trainer import AnnTrainer
import ann_io

n = Network(9, 7, 4)
trainer = AnnTrainer()
trainer.train(n, ['training_sets/corner/' + x for x in ['output1', 'output2', 'output3', 'output4', 'output5', 'output6']], 100)
ann_io.save(n, 'outputfile')
