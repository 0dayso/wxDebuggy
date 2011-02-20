#!/usr/bin/env python
import sys

sys.path.append('../../')

import dev as sugiyama
import unittest

class GraphConnectivityOperations( unittest.TestCase ):

    def setUp(self):
    
        self.V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
        self.E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
                    [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
                    [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
                 ]


    def test_upper_connectivity(self):
        G = sugiyama.Graph( self.V, self.E )
        
        G.build_connection_matrices()
        G.calc_upper_connectivities()
        
        expected = [ [],            # this is to keep indexing sweet
                     [2, 1, 1, 2],
                     [2, 1, 1, 2],
                     [3, 1, 1] ]
                     
        self.assertEquals( G.upper_connectivities, expected )
    
    
    def test_lower_connectivity(self):
        G = sugiyama.Graph( self.V, self.E )
        
        G.build_connection_matrices()
        G.calc_lower_connectivities()
        
        expected = [ [4,2], [1,3,2,0], [1,0,2,2] ]
                     
        self.assertEquals( G.lower_connectivities, expected )
    
       