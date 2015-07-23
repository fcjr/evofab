from the_genome_project import Population
from grid import Grid

population = Population(100, .1, 50, 9, 6, 4, Grid(scale=50, path='corner.test'))
population.iterate(100)
