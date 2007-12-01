#! /usr/bin/env python
"""Genetic Algorithm stuff for instantiation y-placement.

"""
import random
import types

class ga:
    """ Genetic Algorithm Class 

    """

    def __init__(self,
                 num_generations=10, population_size=10, 
                 num_genes=2, bits_per_gene=10, 
                 mutation_rate=0.01, num_crossovers=2,
                 fitness_function=None, num_parents=6,
                 debug=False):
        """  """

        self.num_generations = num_generations
        self.population_size = population_size
        self.num_genes = num_genes
        self.bits_per_gene = bits_per_gene
        self.mutation_rate = mutation_rate
        self.num_crossovers = num_crossovers
        self.debug = debug
        self.num_parents = num_parents
        self.num_random_souls = 2
        
        # A few derived sizes
        self.bits_per_chromosome = self.num_genes * self.bits_per_gene
        
        # Check that we've a fitness function defined.
        assert type(fitness_function) == types.FunctionType
        self.fitness_function = fitness_function

        # A few sanity checks before we proceed
        assert self.population_size >= self.num_parents
        assert self.mutation_rate >= 0.0 and self.mutation_rate <= 1.0
        assert self.bits_per_gene >= 1
        assert ( self.num_crossovers >= 1 and 
                 self.num_crossovers <= self.bits_per_chromosome ) 

        # Population List
        # This is a list of lists: [ <fitness>, [<chromosome_list>] ]
        # we can sort this by fitness easy...
        self.population = []

        self.population = self._initial_population()

    def evolve(self,debug=False, gen_file=False):
        """Run evolution"""

        if gen_file:
            hGA = open("fitnesses.csv","w")
            hGA.write("Generation, Min Fitness, Max Fitness, Average Fitness\n")
            
        if debug:
            x = 20
            print "+" + (" -" * x ) + " +"
            print "|" + "Y-Placement GA".center(x*2+1) + "|"
            print "+" + (" -" * x ) + " +"
        

        # Play $diety, run evolution...
        for gen in range(self.num_generations):
            #print "Generation:", gen

            generation_x = []

            ##
            ## Calculate fitness of each member of the population
            ##
            self._sort_population(gen_file)

            ##
            ## Eugenics...
            ##
            
            # Now that the population is sorted in order of fitness, we'll replace
            # the non-breeding (unfit) souls with a offspring of the top ones. This 
            # is not working out, it's stripping the randomness from the population.
            #
            #  So, what I really want to happen here, is to breed, but have a few 
            # new random souls each generation.
            random_souls_start_index = self.population_size - self.num_random_souls
            for j in range( self.num_parents, random_souls_start_index ):
                # breed one offspring from two parents. we'll use the 'select randomly
                # from a selection' function to select the parents.  the 2nd parent can't
                # be the same as the first, so we'll remove parent 1 from the list when
                # selecting parent 2.
                parent_list = range( self.num_parents )
                parent1_index = random.choice( parent_list )
                del(parent_list[parent1_index])
                parent2_index = random.choice( parent_list )

                parent1 = self.population[parent1_index][1]
                parent2 = self.population[parent2_index][1]

                offspring1,offspring2 = self._breed(parent1, parent2)
                self.population[j] = [ 0, offspring1 ]
 
 
            #  Keep randomness in population by creating a few random souls each
            # generation
            for j in range( random_souls_start_index, self.population_size ):
                self.population[j][1] = self._random_chromosome()
                

            ##
            ## Introduce some mutations
            ##
            self._mutation()


        # Now choose the fittest as our result...
        self._sort_population(gen_file)
        
        return self.population[0][1]     
        

#######################################################################################
####  'Private' methods
#######################################################################################
    def _initial_population(self, debug=False):
        """Create an initial random population"""

        # Set up the array to hold the genome of the population
        chromosome_size = self.num_genes * self.bits_per_gene
        population = [0] * self.population_size
        for i in range( self.population_size ):
            population[i] = [ 0, self._random_chromosome() ]

        if debug:
            for soul in population:
                print soul
         
        return population
        

    def _print_population(self):
        """Print out the population"""
        for soul in self.population:
            print soul
        

    def _random_chromosome(self):
        """Return a random chromosome """
        
        chromosome = []
        for i in range( self.num_genes * self.bits_per_gene ):
            chromosome.append( random.randrange(0,2) )

        return chromosome
        

    def _calc_fitnesses(self):
        """Calculate the fitness level of each member of the population"""

        for j in range( len(self.population) ):
            fitness = self.fitness_function( self.population[j][1] ) # pick the chromo part
            self.population[j][0] = fitness # we'll sort by this index

        return
   

    def _sort_population(self, gen_file=False, debug=False):
        """Sort the population based on fitness """

        # First, calc the fitness of each soul in the population
        self._calc_fitnesses()
        
        #  Write results to file? Useful for debug or determining GA config for
        # specific problems
        if gen_file:
            min_fitness, max_fitness, avg_fitness = self._get_stats()
            hGA.write("%d,%d,%d,%f\n" % (gen, min_fitness, max_fitness, avg_fitness ) )
            
        # Sort population
        self.population.sort()
        self.population.reverse()            

        if debug:
            self._print_population()
        
        return


    def _breed(self, parent1, parent2, debug=False ):
        """Breed two parents"""

        bits_per_chromosome = self.num_genes * self.bits_per_gene 

        # Calculate crossover points. 
        #   I have to make sure their in assending order, eg: [2, 23 ] is good 
        # and [14,2] is bad.
        #  To this end, I'll keep the value of the previous calculated crossover 
        # point and pick a random number from this to the length of the chromosome 
        crossover_indexes = []
        prev_crossover = 0 # lower limit for crossover range
        for i in range( self.num_crossovers ):
            xindex = random.randrange(prev_crossover, bits_per_chromosome) 
            crossover_indexes.append( xindex )
            prev_crossover = xindex

        babie1 = []
        babie2 = []

        # babies
        cross = True
        cl = 0

        if debug:
            print "- " * 20
            print "Parent1:", parent1
            print "Parent2:", parent2

        for ci in crossover_indexes:

            if cross:            
                babie1.extend(parent1[cl:ci])
                babie2.extend(parent2[cl:ci])
            else:
                babie1.extend(parent2[cl:ci])
                babie2.extend(parent1[cl:ci])
        
            if debug:
                print "crossover point:", ci
                print "Babie1:", babie1
                print "Babie2:", babie2

            cl = ci
            cross = not cross


        if cross:            
            babie1.extend(parent1[cl:])
            babie2.extend(parent2[cl:])
        else:
            babie1.extend(parent2[cl:])
            babie2.extend(parent1[cl:])
         
        if debug:
            print "Babie1: ", babie1
            print "Babie2: ", babie2
       
        assert len(babie1) == bits_per_chromosome
        assert len(babie2) == bits_per_chromosome

        return babie1, babie2


    def _mutation(self,debug=False):
        """Mutation """
        
        bits_per_chromosome = self.num_genes * self.bits_per_gene      

        for i in range( len(self.population) ):
            flip_if_one = [0] *  bits_per_chromosome
            flip_if_one = [ self._flag_mutation(i) for i in flip_if_one ] # list comprehension

            # now write the (mutated?) soul back into the population
            self.population[i][1] = map( self._mutate, self.population[i][1], flip_if_one )
 
        return

    
    def _mutate(self, soul, flip_if_one):
        """Use maps to flip bits in the cromosome"""
        
        if flip_if_one:
            return soul
        else:
            if soul:
                return 0
            else:
                return 1



    def _flag_mutation(self,dummy):
        return random.random() <= self.mutation_rate


    def _get_stats(self):
        """Collect some stats for the current population"""
        
        fitnesses = []
        for fitness,soul in self.population:
            fitnesses.append(fitness)
            
        assert len(fitnesses) == self.population_size
        
        max_fitness = max(fitnesses)
        min_fitness = min(fitnesses)
        avg_fitness = sum(fitnesses,0.0) / len( fitnesses )
        
        return min_fitness,max_fitness,avg_fitness

### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
### 
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
if __name__ == '__main__':

    def fitness_function( soul, debug=False):
        
        fitness = 0
        for i in soul:
            if i == 1:
                fitness += 1

        if debug:
            print fitness, ":", soul

        return fitness

    
    myGA = ga(fitness_function=fitness_function, 
              num_generations=10,
              population_size=50,
              num_parents=10,
              mutation_rate=0.1)
    print myGA.evolve()

    
