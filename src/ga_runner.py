from ann_genetic_algorithms import AnnPopulation
from grid import Grid

population = AnnPopulation(10, .1, 2, 9, 6, 4, Grid(scale=50, path='corner.test'))
population.iterate(100)
