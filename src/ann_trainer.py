from ann import Network
import ann_io

import csv

camera_headers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
output_headers = ['x velocity', 'y velocity']

downsample_constant = 100

class TrainingSetLoader:

    def __init__(self, path):
        self.path = path

    def read(self):
        """ returns (camera_vals, x,y velocities) """

        with open(self.path, 'r') as to_read:
            reader = csv.reader(to_read)
            _ = reader.next()
            camera_vals = []
            velocities = []
            for row in reader:
                camera_vals.append(row[:len(camera_headers)])
                velocities.append(row[len(camera_headers):][0])
                velocities = [[int(x) for x in string] for string in velocities]
        camera_vals = camera_vals[::downsample_constant]
        velocities = velocities[::downsample_constant]
        return (
                [[float(x) for x in row] for row in camera_vals],
                velocities
                )

class AnnTrainer:

    def train(self, n, paths_to_training_sets, iterations=8000):
        n.inputs = []
        n.targets = []
        for path in paths_to_training_sets:
            loader = TrainingSetLoader(path)
            inputs, targets = loader.read()
            n.inputs += inputs
            n.targets += targets
            #print 'loaded', path
        n.test()
        n.train(iterations)
