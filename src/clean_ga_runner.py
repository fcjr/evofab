from the_clean_genome_project import Population
from grid import Grid

population = Population(60, .1, 30, 9, 7, 4, Grid(scale=50, path='corner.test'))
population.iterate(600)
