from ann import Unit, Network, Connection
import pickle

def save(ann, filepath):
    with open(filepath, 'w') as outputfile:
        pickle.dump(ann, outputfile)

def load(filepath):
    with open(filepath, 'r') as inputfile:
        ann = pickle.load(inputfile)
    return ann
