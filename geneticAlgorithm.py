# A file that contains the genetic algorithm implementation

import numpy as np
import midiDriver
import audioRecorder
import audioComparator

class GeneticAlgorithm:

  # internal chromosome class
  class Chromosome:
    def __init__(self, g=None, genes=[]):
      # g is the number of genes per chromosome
      if g == None:
        g = 10
      if genes != []:
        self.genes = genes
      else:
        self.genes = np.random.randint(0, 2, g)
      self.fitness = None

    def __str__(self):
      return str(self.genes)
        
  
  # Initializes the genetic algorithm population
  # - pop_size: the population size
  # - num_genes: the number of genes per individual
  def __init__(self, pop_size=10, num_genes=10):
    self.parents = []
    self.population = []
    for i in range(pop_size):
      C = self.Chromosome(num_genes)
      self.population.append(C)

  # updates the fitness score for the entire population
  def update_fitness(self):

    # 1. send params (genes) to Massive
    # 2. record audio from Massive
    # 3. compare recording to target sound
    for i in self.population:
      i.fitness = manager.calc_GA_fitness
  
  def sort_population(self):
    self.population.sort(key=lambda c: c.fitness)
  
  def select(self, style='greatest'):
    # if parents % 2 != 0:
    #   print('parents must be multiple of 2')
    self.sort_population()
    for i in range(2):
      # higher probability to select most-fit chromosomes
      if style == 'greatest': 
        if np.random.randint(0, 10) < 8:
          self.parents.append(self.population[-1])
        else: # select random chromosome in population
          self.parents.append(
              self.population[np.random.randint(0, len(self.population))])
          
  def crossover(self, radix=None):
    # define radix as crossover point inside chromosome
    radix = np.random.randint(2, len(self.population)-2)
    # swap parent's genes and create children
    parent1, parent2 = self.parents[0], self.parents[1]
    child1 = self.Chromosome(genes=np.concatenate((parent1.genes[:radix], parent2.genes[radix:])))
    child2 = self.Chromosome(genes=np.concatenate((parent2.genes[:radix], parent1.genes[radix:])))
    # add children to front of population
    self.population.append(child1)
    self.population.append(child2)

  def mutation(self):
    # low probability of mutation
    if np.random.randint(0, 10) > 1:
      return
    child1, child2 = self.population[-1], self.population[-2]
    i = np.random.randint(2, 10) # select random number of genes to mutate
    for c in (child1, child2):
      for x in range(i):
        if i >= len(c.genes): # restrict i to be within length of chromosome
          i -= len(c.genes)
        c.genes[i] = 1 if c.genes[i] == 0 else 0
        i += 1

  def trim(self, style='greatest'):
    if style == 'greatest':
      # remove least fit chromosomes
      del self.population[:2]

  def fitness_difference(self):
    return abs(self.population[-1].fitness - self.population[0].fitness) 

  def step(self, num_steps=1, fitness='sum', selection='greatest', 
           crossover_point=None, trim='greatest'
           ):
    for i in range(num_steps):
      self.update_fitness(fitness)
      self.select(selection)
      self.crossover(crossover_point)
      self.mutation()
      self.trim(trim)
      self.update_fitness(fitness)
      
  def __str__(self):
    pop = []
    for i in range(len(self.population)):
      pop.append(str(i) + ': ' + str(self.population[i])
      + ' fit: ' + str(self.population[i].fitness))
    return str(pop)