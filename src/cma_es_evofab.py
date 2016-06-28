from cma import fmin
from numpy import ndarray
from ann_runner import AnnRunner
from ann import *
from grid import Grid

reward_for_correct = 20
punishment_for_incorrect = 5

def objective_function(genotype, ob):
    genotype = genotype.tolist()
    phenotype = ob.express(genotype)
    fitness = 0
    for ideal_grid, actual_grid in phenotype:
        for ideal_row, actual_row in zip(ideal_grid, actual_grid):
            for ideal, actual in zip(ideal_row, actual_row):
                if ideal == 1 and actual == 1:
                    fitness += reward_for_correct
                elif ideal == 0 and actual == 1:
                    fitness -= punishment_for_incorrect
    fitness = fitness * -1 #kludge because CMA-es wants to minimize
    return fitness/50.0


class Evolver:
    def __init__(self, goal_list, cell_scale=30, units_per_cell=10, visual=True, printer_runtime=300, num_input=9, num_hidden=18, num_output=4):
        self.goal_list = [Grid(scale=cell_scale, path=val) for val in goal_list]
        self.visual = visual
        self.units_per_cell = units_per_cell
        self.num_input = num_input #note: might not need these since 
        self.num_hidden = num_hidden #we're already making the ann here
        self.num_output = num_output
        self.ann = Network(num_input, num_hidden, num_output)
        self.printer_runtime = printer_runtime
        
    def evolve(self, initial_value=None, initial_stddev=20):
        if not initial_value:
            initial_value = [random.randrange(-10, 10) for x in self.ann.allConnections]
        else:
            assert(len(self.ann.allConnections) == len(initial_value))
        fmin(objective_function, initial_value, initial_stddev, args=tuple([self]), restarts=10, options={"ftarget":-6.0})
        return

    def express(self, genotype):
        result = []
        self.ann.allConnections = genotype
        for world in self.goal_list:
            if self.visual:
                from gui_ann_runner import GuiAnnRunner
                runner = GuiAnnRunner(world, self.units_per_cell)
            else:
                runner = AnnRunner(world, self.units_per_cell)
            ideal_grid, actual_grid = runner.run(self.ann, iterations=self.printer_runtime)
            result.append((ideal_grid.grid, actual_grid.grid))
        return result

if __name__ == "__main__":
    e = Evolver(goal_list=['worlds/angles1.test'
                          ])
    e.evolve()
