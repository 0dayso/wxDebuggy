
class Matrix(object):
    """ A Class to model a matrix for Sugiyama Layouts.
    A collection of these matrices will form the Martix Realisation
    of a graph. 
    
    Some modifications are made to handle circuits, namely:
     * Edges are grouped if they belong to the same block
     * Each block has input and output vertices
     
    """
    
    def __init__(self, row_blocks, col_blocks, edges):
        self.row_blocks = row_blocks
        self.col_blocks = col_blocks
        self.row_vertices = []  # flattened 
        self.col_vertices = []
        self.edges = edges
        self.update()
        
        
    def get_size(self):
        """ Return the size of the connectivity matrix."""
        return (self.c_rows, self.c_cols)
        
        
    def update(self):
        """ Recalculate the recalculable."""

        self.row_vertices = []
        self.col_vertices = []
        
        # Flatten the connections        
        for block in self.row_blocks:
            for out_pin in block.outputs:
                self.row_vertices.append( '.'.join([block.name, out_pin]) )
        for block in self.col_blocks:
            for in_pin in block.inputs:
                self.col_vertices.append( '.'.join([block.name, in_pin]) )
            
        self.c_rows = len(self.row_vertices)
        self.c_cols = len(self.col_vertices)

        self.M = self._build_connection_matrix()
        
        self.row_barycentres = self._calc_row_barycentres()
        self.col_barycentres = self._calc_col_barycentres()
        
        self.block_row_barycentres = self._calc_block_row_barycentres()
        self.block_col_barycentres = self._calc_block_col_barycentres()
        
        
    def get_crossover_count(self):
        """ Return the crossover count of the connectivity matrix. """
        return self._calc_crossover_count()
        
        
    def copy(self):
        """ Return a deepish copy of the instance."""
        M_copy = Matrix( list(self.row_blocks),
            list(self.col_blocks), list(self.edges) )

        return M_copy   
            
        
    def _build_connection_matrix(self):
        """ Initialise the connection matrix for this layer. """
        
        M = []

        # Size matrix and initialise to zero
        for i in xrange( self.c_rows ):
            row = [0] * self.c_cols
            M.append(row)

        # Fill in the connections
        for ( (source, o_pin), (sink, i_pin) ) in self.edges:
            if source == '_iport':
                source_name = '.'.join([o_pin, o_pin])
            else:
                source_name = '.'.join([source, o_pin])
            if sink == '_oport':
                sink_name = '.'.join([i_pin, i_pin])
            else:
                sink_name = '.'.join([sink, i_pin])
                
            row_index = self.row_vertices.index( source_name )
            col_index = self.col_vertices.index( sink_name )
            M[row_index][col_index] = 1
            
        return M

        
    def _calc_row_barycentres(self):
        """ Calculate the row barycentres of the matrix. """
 
        barycentres = []
        
        for k in xrange(self.c_rows):
            numer = 0.0
            denom = 0.0
            
            for l in xrange(self.c_cols):
                numer += (l+1) * self.M[k][l]
                denom += self.M[k][l]
                
            if denom:
                barycentre = numer / denom
            else:
                barycentre = 0.0
                
            barycentres.append(barycentre)
        
        return barycentres
                
    
    def _calc_block_row_barycentres(self):
        """ Calculate the block row barycentres of the matrix. 
        
        These are the average of the barycentres of the output ports 
        of each row block.
        """
        i = 0
        barycentres = []
        for block in self.row_blocks:
            bc_tmp = 0
            n_ports = len(block.outputs)
            for j in xrange(n_ports):
                bc_tmp += self.row_barycentres[i]
                i += 1
            bc_tmp /= n_ports
            barycentres.append(bc_tmp)
            
        return barycentres
        
        
    def _calc_block_col_barycentres(self):      
        """ Calculate the block col barycentres of the matrix. 
        
        These are the average of the barycentres of the input ports 
        of each col block.
        """
        i = 0
        barycentres = []
        for block in self.col_blocks:
            bc_tmp = 0
            n_ports = len(block.inputs)
            for j in xrange(n_ports):
                bc_tmp += self.col_barycentres[i]
                i += 1
            bc_tmp /= n_ports
            barycentres.append(bc_tmp)
            
        return barycentres
        
        
    def _calc_col_barycentres(self):
        """ Calculate the column barycentres of the matrix. """
        
        barycentres = []
        
        for l in xrange(self.c_cols):
            numer = 0.0
            denom = 0.0
            
            for k in xrange(self.c_rows):
                numer += (k+1) * self.M[k][l]
                denom += self.M[k][l]
                
            if denom:
                barycentre = numer / denom
            else:
                barycentre = 0.0
                
            barycentres.append(barycentre)
            
        return barycentres
        
        
    def _calc_k(self, j, k):
        """ Calculate the crossings between an ordered pair of vertex rows.
        Calculates k( r(u,v), r(v,u) ) """
        q = self.c_cols
        k_jk = 0
        
        for a in xrange(0, self.c_cols-1 ):  # 0 ... q-2
            for b in xrange(a+1, self.c_cols ): # a+1 ... q-1
                k_jk += self.M[j][b] * self.M[k][a]
        
        return k_jk


    def _calc_crossover_count(self):
        """ Find out how many crossovers this connectivity matrix has."""
        K_M = 0
        
        for j in xrange(0, self.c_rows-1):
            for k in xrange(j+1, self.c_rows):
                K_M += self._calc_k( j, k )
        
        return K_M
        
        
    def _new_row_order(self, new_block_order):
        """ Reorder the connection matrix based on a new ordering. 
        There are 4 stages to this:
        #1: reorder the connection matrix rows
        #2: reorder the barycentre numbers to match te new row order
        #3: reorder the block barycentre numbers
        #4: recalculate the flattened column barycentres
        #5: recalculate the block column barycentres
        """

        # Rejigg the connection matrix for the new order. Reorder flattened 
        # vertex names too
        i = 0
        row_data = zip( self.row_vertices, self.M, self.row_barycentres )
        row_dict = {}
        for block in self.row_blocks:
            for port in block.outputs:
                row_dict[(block.name, port)] = row_data[i]
                i += 1
    
        new_M = []
        new_vertices = []
        new_bcs = []
        for block in new_block_order:
            for port in block.outputs:
                vertex, conns, bcs = row_dict[(block.name, port)]            
                new_M.append(conns)
                new_vertices.append(vertex)
                new_bcs.append(bcs)
        self.M = new_M
        self.row_vertices = new_vertices
        self.row_barycentres = new_bcs
                
        # Rejig the block level barycentre numbers
        bc_dict = {}
        for block, bcs in zip( self.row_blocks, self.block_row_barycentres):
            bc_dict[block.name] = bcs
            
        new_bc = []
        for block in new_block_order:
            new_bc.append( bc_dict[block.name] )
        self.block_row_barycentres = new_bc
        
        self.row_blocks = new_block_order
        
        # Recalculate the column barycentre numbers
        self.col_barycentres = self._calc_col_barycentres()
        self.block_col_barycentres = self._calc_block_col_barycentres()        
        
        
    def barycentre_row_reorder(self):
        """ Reorder the rows based on their barycentres. """
        
        # Find the new vertice order
        dec = [ ( bc, v ) for (v, bc)  in zip (
             self.row_blocks, self.block_row_barycentres ) ]
        dec.sort()
        new_vertice_order = [ v for (bc, v) in dec ]
         
        self._new_row_order( new_vertice_order )

        
    def _new_col_order(self, new_block_order):
        """ Reorder the connection matrix based on a new ordering. """
        
        # Flip cols into rows to make them easier to work with
        cols = zip( *self.M )
        
        # Rejigg the connection matrix for the new order. Reorder flattened 
        # vertex names too
        i = 0
        col_data = zip( self.col_vertices, cols, self.col_barycentres )
        col_dict = {}
        for block in self.col_blocks:
            for port in block.inputs:
                col_dict[(block.name, port)] = col_data[i]
                i += 1
                
        import pprint
        pprint.pprint(col_data)
        new_M = []
        new_vertices = []
        new_bcs = []
        print "NBO", new_block_order
        for block in new_block_order:
            for port in block.inputs:
                print block.name, port
                vertex, conns, bcs = col_dict[(block.name, port)]
                new_M.append(conns)
                new_vertices.append(vertex)
                new_bcs.append(bcs)
        self.col_vertices = new_vertices
        self.col_barycentres = new_bcs
        pprint.pprint(new_M)
        self.M = [ list(a) for a in zip(*new_M) ] # zip() produces tuples, need lists
        pprint.pprint(self.M)
        # Rejig the block level barycentre numbers
        bc_dict = {}
        for block, bcs in zip( self.col_blocks, self.block_col_barycentres):
            bc_dict[block.name] = bcs
            
        new_bc = []
        for block in new_block_order:
            new_bc.append( bc_dict[block.name] )
        self.block_col_barycentres = new_bc
        
        self.col_blocks = new_block_order
        
        # Recalculate the column barycentre numbers
        self.row_barycentres = self._calc_row_barycentres()
        self.block_row_barycentres = self._calc_block_row_barycentres() 
        
                
    def barycentre_col_reorder(self):
        """ Reorder the columns based on their barycentres. """
        
        # Find the new vertice order
        dec = [ ( bc, v ) for (v, bc)  in zip( 
            self.col_blocks, self.block_col_barycentres ) ]
        dec.sort()
        new_vertice_order = [ v for (bc, v) in dec ]
        
        self._new_col_order(new_vertice_order)
        
        
    def _reversion(self, vertices, barycentres ):
        """ Vertice Reversion"""
        
        new_vertice_order = []
        vertice_group = [ vertices[0] ]
       
        for i in xrange(1, len(barycentres) ):
            if barycentres[i] == barycentres[i-1]:
                vertice_group.append( vertices[i] )
            else:
                vertice_group.reverse()
                new_vertice_order.extend(vertice_group)
                vertice_group = [ vertices[i] ]

        vertice_group.reverse()
        new_vertice_order.extend(vertice_group)
        
        return new_vertice_order
          
          
    def row_reversion(self):
        """ Reverse rows sequences that have equal barycentres."""
        if not self._barycentres_are_monotonic(self.row_barycentres):
            new_order = self._reversion( self.row_vertices, self.row_barycentres )
            self._new_row_order( new_order )

     
    def col_reversion(self):
        """ Reverse columns with equal barycentre numbers."""
        if not self._barycentres_are_monotonic(self.col_barycentres):
            new_order = self._reversion( self.col_vertices, self.col_barycentres )
            self._new_col_order( new_order )
                     
    
    def _barycentres_are_monotonic(self, barycentres):
        """ Barycentre list is always on the increase?"""
        
        if len(barycentres) == 1:
            return True
            
        for i in xrange(1, len(barycentres) ):
            if barycentres[i] <= barycentres[i-1]:
                return False
                
        return True
        
        
    def row_barycenters_are_monotonic(self):
        return self._barycentres_are_monotonic(self.row_barycentres)
        
        
    def col_barycenters_are_monotonic(self):
        return self._barycentres_are_monotonic(self.col_barycentres)
                      

    def __str__(self):
        """ Printout
        Print the connection matrix with row and col headers, and with
        row and column barycentre numbers just like in Sugiyama's paper.
        """
  
        repr_str_list = ['\nConnection Matrix:']
        
        first_line = '%10s' % (' ')
        for vertice in self.col_vertices:
            first_line += '%10s' % (vertice )
        repr_str_list.append(first_line)
 
        for j in xrange(self.c_rows):
            line = '%10s' %(self.row_vertices[j])
            for conn in self.M[j]:
                line += '%10s' % (conn)
            line += ' : %.1f' % (self.row_barycentres[j])
            repr_str_list.append(line)
        
        last_line = '%10s' %('')
        for bc in self.col_barycentres:
            trunc = '%0.1f' % (bc)
            last_line += '%10s' % (trunc) 
        repr_str_list.append(last_line)
           
        # Add crossover count:
        repr_str_list[3] += "    K = %d" % ( self.get_crossover_count() )
        return '\n'.join(repr_str_list)
        
        
    def pretty(self):
        """ Return a fancy string representation of the matrix 
        __str__() can't use unicode chars, so this...
        """
        
        str_list = self.__str__().split('\n')
        str_list[4] = str_list[4].split('    K =')[0]
        
        # Add block barycentres
        self.__str_add_block_row_barycentres(str_list)
        self.__str_add_block_col_barycentres(str_list)

        str_list[1] = str_list[1].replace('Matrix:',
            'Matrix (%0d crossovers)' % self.get_crossover_count() )
        return '\n'.join(str_list)
      
                          
    def __str_add_block_row_barycentres(self, str_list):
        """ Add the block barycenters to the matrix string representation. """
        
        i = 0
        i_str = 3
        for block in self.row_blocks:
            n = len(block.outputs)
            if n == 1:
                str_list[i_str] += u' \u2500\u2500 %.3f' % (self.block_row_barycentres[i])
            else:
                str_list[i_str] += u' \u252c\u2500 %.3f' % (self.block_row_barycentres[i])
                for j in xrange(n-2):
                    i_str += 1
                    str_list[i_str] += u' \u2502'
                i_str += 1
                str_list[i_str] += u' \u2518'
            i += 1
            i_str += 1      
          
          
    def __str_add_block_col_barycentres(self, str_list, N=10):
        """ Add col block barycentres to end of the string representation."""
        graphics_line = [ (' ' * N) ]
        barycentre_line = [ (' ' * N ) ]
        leadin = ' ' * (N-2)
        
        i = 0
        i_str = 3
        for block in self.col_blocks:
            n = len(block.inputs)
            trunc = '%0.1f' % (self.block_col_barycentres[i])
            if n == 1:
                graphics_line.append( leadin + u'\u251c ' )
                barycentre_line.append('%10s' % (trunc))
            else:
                graphics_line.append( leadin + u'\u251c\u2500' )
                barycentre_line.append('%10s' % (trunc) )
                for j in xrange(n-2):
                    graphics_line.append( (u'\u2500' * N) )
                    barycentre_line.append( (' ' * N ) )

                graphics_line.append( ( u'\u2500' * (N-2) ) + u'\u2518 ' )
                barycentre_line.append( (' ' * N ) )
            i += 1

        str_list.append( ''.join(graphics_line) )
        str_list.append( ''.join(barycentre_line) )
                    
        
