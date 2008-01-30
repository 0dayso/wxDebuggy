#! /usr/bin/env python
""" Generic Genetic Algorithm Class"""

import random
import types

class ga:
    """A Generic Genetic Algorithm Class

    A generic GA class which implements breeding through crossovers and 
    random mutations.  
    
    Usage
    --------------------------------------------------------------------
      Initialise an instance of this class with the desired population 
    size, etc and a fitness function.  Then call the 'evolve' method to
    run the GA, which will return the fittest chromosome on completion
    of the algorithm.
    
      Passing 'gen_file=True' as an argument to the 'evolve' method will
    enable the creation of a stats file for the GA run.  This may be 
    useful for fine-tuning the GA configuration to solve the problem at
    hand.

    A Note on the Fitness Function:
    --------------------------------------------------------------------
      As every application will have its own measure of fitness, the
    fitness function cannot be generalised. Therefore to use this class,
    a fitness function specific to the task at hand must be written and
    passed to this class on instantiation.  An Assertion will check that
    a valid function is supplied.
    """

    def __init__(self,
                 num_generations=10, population_size=10, 
                 num_genes=2, bits_per_gene=10, 
                 mutation_rate=0.01, num_crossovers=2,
                 fitness_function=None, num_parents=6, 
                 num_elite=2,
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
        self.num_elite = num_elite
        self.num_random_souls = 0
        
        # A few derived sizes
        self.bits_per_chromosome = self.num_genes * self.bits_per_gene
        
        # Check that we've a fitness function defined.
        assert type(fitness_function) == types.FunctionType
        self.fitness_function = fitness_function

        # A few sanity checks before we proceed
        assert self.population_size >= self.num_parents
        assert self.population_size >= self.num_elite
        assert self.mutation_rate >= 0.0 and self.mutation_rate <= 1.0
        assert self.bits_per_gene >= 1
        assert ( self.num_crossovers >= 1 and 
                 self.num_crossovers <= self.bits_per_chromosome ) 

        # Population List
        # This is a list of lists: [ <fitness>, [<chromosome_list>] ]
        # we can sort this by fitness easy...
        self.population = []

        self.population = self._initial_population()
        self.offspring  = list(self.population)
        
        self.hGA = None  # GA info file handle
        self.gen = 0     # generation counter
        
        
    def evolve(self,debug=False, gen_file=False):
        """Run Evolution"""

        if gen_file:
            self.hGA = open("fitnesses.csv","w")
            self.hGA.write("Generation, Min Fitness, Max Fitness, Average Fitness\n")
            
        if debug:
            x = 20
            print "+" + (" -" * x ) + " +"
            print "|" + "Y-Placement GA".center(x*2+1) + "|"
            print "+" + (" -" * x ) + " +"
        

        # Play $diety, run evolution...
        for self.gen in range(self.num_generations):

            ## Calculate fitness of each member of the population
            self._sort_population(gen_file)    
        
            # Print the fittest...
            self.fitness_function( self.population[0][1], display=True )
                      
            # Breeding
            self._new_generation()
              
            ##  Keep randomness in population by creating a few random souls each
            # generation. I'm not sure how effective of necessary this is.
            random_souls_start_index = self.population_size - self.num_random_souls
            for j in range( random_souls_start_index, self.population_size ):
                self.population[j][1] = self._random_chromosome()
                
            ## Introduce some mutations (and hope we don't get zombies...)
            self._quicker_mutation()


            
        # ---------------------------------------------------- End of generations loop
        
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
            new_chromosome = self._random_chromosome()
            new_fitness    = self._calc_fitness( new_chromosome )
            population[i] = [ new_fitness, new_chromosome ]
            
        if debug:
            for soul in population:
                print soul
         
        return population
        

    def _print_population(self):
        """Print out the population, each on a newline"""
        print "Population"
        for soul in self.population:
            print soul
        
        
    def _print_offspring(self):
        """Print out the offspring, each on a newline"""
        print "Offspring"
        for soul in self.offspring:
            print soul
       
            
    def _random_chromosome(self):
        """Return a random chromosome """
        
        chromosome = []
        for i in range( self.num_genes * self.bits_per_gene ):
            chromosome.append( random.randrange(0,2) )

        return chromosome
        
             
    def _calc_fitness(self, soul):
        """Calculate the fitness of a given member ot the population"""
        
        fitness = self.fitness_function( soul )
        return fitness  
        

    def _calc_fitnesses(self):
        """Calculate the fitness level of each member of the population
        
         This uses the fitness function supplied to the class instance to 
        get a number for the fitness of each soul in the population.
        """

        for j in range( len(self.population) ):
            fitness = self.fitness_function( self.population[j][1] ) # pick the chromo part
            self.population[j][0] = fitness # we'll sort by this index

        return
   

    def _sort_population(self, gen_file=False, debug=False):
        """Sort the population based on fitness.
        
        This assumes that the bigger the fitness number, the fitter the soul.
        """

        # First, calc the fitness of each soul in the population
        self._calc_fitnesses()
        
        #  Write results to file? Useful for debug or determining GA config for
        # specific problems
        if gen_file:
            min_fitness, max_fitness, avg_fitness = self._get_stats()
            self.hGA.write("%d,%d,%d,%f\n" % (self.gen, min_fitness, max_fitness, avg_fitness ) )
            print "Generation %d, max=%d, avg=%f" % ( self.gen, max_fitness, avg_fitness ) 
                
        # Sort population
        self.population.sort()
        self.population.reverse()            

        if debug:
            self._print_population()
        
        return


    def _new_generation(self):
        """Breed a new generation of souls
        
          Now that the population is sorted in order of fitness, we'll replace
        most of the non-breeding (unfit) souls with a offspring of the top ones.
        One of the potential parents is taken from the top 'self.num_parents' of
        the population.  The other parent is taken from anywhere in the population.
        
          The bottom 'self.num_random_souls' of the population will be replaced with 
        random population members.  All other souls will be replaced with the 
        offspring of parents.            
        """
            
        random_souls_start_index = self.population_size - self.num_random_souls
        
        for j in range(0, random_souls_start_index, 2):
            
            ## Breed two offspring from two parents.
            # Calculate parent indexes
            parent1_index = random.randrange( self.num_parents )
            parent1 = self.population[parent1_index][1]
            
            parent2_index = random.randrange( self.num_parents )
            parent2 = self.population[parent2_index][1]


            # ... and store the products of their loving...
            offspring1,offspring2 = self._breed(parent1, parent2)
            self.offspring[j] = [ 0, offspring1 ]
            if len(self.population) != j+1:
                self.offspring[j+1] = [ 0, offspring2 ]            
        
        
        # Now update the population with the new generation
        num_offspring = self.population_size - self.num_elite
        self.population[self.num_elite:] = self.offspring[:num_offspring]

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

        
    def _quicker_mutation(self,debug=False):
        """Mutation.
        
        Instead of generating a random number for each bit in each member of the
        population, generate only a few. 
        
        First, using the size of the chromosome and the mutation rate, determine
        the max number of bits that's likely to mutate.  Then, use this number as
        the upper limit when randomly generating a number of bits to mutate.  
        Then for each bit were mutating, generate a random locus.     
        
        Shit. This doesn't work if the max_num_bits turns out to be less than 1.  
        """
        
        bits_per_chromosome = self.num_genes * self.bits_per_gene      
        max_bits_to_mutate = bits_per_chromosome * self.mutation_rate
        print "B2M", max_bits_to_mutate, bits_per_chromosome
        bits_to_mutate = random.randrange( int(max_bits_to_mutate) )
        print "B2M", bits_to_mutate
        
        for i in range( bits_to_mutate ):
                            
            locus = random.randrange(bits_per_chromosome)
            soul = self.population[i][1] # pointer/reference?  
            
            if debug: print soul                     
            soul[locus] = soul[locus] ^ 1                 
            if debug: print soul, locus
                        
        
        return
        
        
    def _mutation(self,debug=False):
        """Mutation
        
         Each bit on each gene of each member of the population has
        'self.mutation_rate' chance of being flipped.
        """
        
        bits_per_chromosome = self.num_genes * self.bits_per_gene      

        for i in range( len(self.population) ):
        
            #  Build a vector to flip bits in the chromosome. A 'True' in this 
            # vector will flip the corresponding bit in the current chromosome.
            flip_if_one = [0] *  bits_per_chromosome
            flip_if_one = [ self._flag_mutation(i) for i in flip_if_one ] # list comprehension

            # Now write the (possibly mutated) soul back into the population
            a = map( self._mutate, self.population[i][1], flip_if_one )
            if debug:
                mutation_count = 0
                for x in flip_if_one:
                    if x:
                        mutation_count += 1
                print "Mutations:", mutation_count
                #print flip_if_one
                #print "Before :", self.population[i][1]
                #print "After  :", a
            self.population[i][1] = a
            
        return

    
    def _mutate(self, soul, flip_if_one):
        """Used in map operation to flip bits in the chromosome"""
        
        if flip_if_one:
            if soul:
                return 0
            else:
                return 1
        else:
            return soul



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


    def hanning_distance( soul, debug=False, display=False):
        """ Fitness is the distance away from the string
        
        Don't tell me Unicode is going to bollox this up... """
  
        match_this = 'This is a string of length 50 characters. Honestly'
        #match_this = 'Th'
        soul_str   = ''.join( [str(bit) for bit in soul ] )
        
        string = ""
        distance = 0
        fitness = 0
        
        if debug:
            print soul_str
        
        for i in range( len(match_this ) ):
            i1,i2 = (i*7)+7, i*7
            #print "i1,i2", i1,i2

            ga_ord = int( soul_str[i2:i1], 2)

            if ga_ord >= 32:
                string += chr(ga_ord)             
            else:
                string += '.'
                
            distance += abs( ga_ord - ord(match_this[i]) )

            # it seems that if you try to display chr(14), the terminal
            # screws up...
            if debug:
                print '   "%s"' % ( soul_str[i2:i1] ), ga_ord, string[-1]
                print "   Match '%s' (%d) with '%s' (%d): Distance: %d" % (
                     match_this[i], ord(match_this[i]),
                     string[-1], ga_ord , 
                     abs( ga_ord - ord(match_this[i]) )
                     ) 
                print "  ", string

                    
            if match_this[i] == chr(ga_ord):
                fitness += 1
                
            
        if display:
            print string, fitness
            #myGA.hGA.write(":'%s'\n" % ( string ) )   
                       
        # fitness = (50*128)-distance
        assert fitness >= 0
        return fitness
    
    
    myGA = ga(fitness_function=hanning_distance, 
              bits_per_gene=7,  # 8-bits of y-axis...
              num_genes=50,     # 50 instantiations...
              num_generations=100,
              population_size=1000,
              num_crossovers=1,
              num_parents=100,
              num_elite=10,
              mutation_rate=0.001)
              
    print myGA.evolve(gen_file=True)

