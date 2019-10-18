""" implementing a basic network according to NEAT dna
 this will be functional: we will not have network/node classes etc...
 the function will decode and run the dna to produce the output """

""" 
        IMPROVEMENT SUGGESIONS 
1
should implement genes of the same type as a 2D list where each row is a new gene with its properties, 
this way we could access a certain property of all the genes simply by genes[:][property] 
"""

import random


def node_gene(node_type, id):
    """ node_type: input, output or hidden
    returns a node's genome of the given type
    the genome structure is the following """
    gene = {'type': node_type, 'id':0}


def connection_gene(input_node_id, output_node_id, innovation_number, weight=1):
    gene = {'input':input_node_id, 'output':output_node_id, 'weight':weight,
            'expressed':True, 'innovation_number':innovation_number}


# genome = {'node_genes':{'input_nodes':[], 'hidden_nodes':[], 'output_ndoes':[]}, 'connection_genes':[]}
genome = {'node_genes':[], 'connection_genes':[]}

def next_node_id(genome):       # TODO this can be optimised by following suggestion 1 (see top)
    """ returns the next node id to be used (one larger than the current largest) """
    return max([node['id'] for node in genome['node_genes']]) + 1


def add_connection(genome, innovation_number, weight=1):
    """ adds a random connection between two nodes """
    node0 = random.choice(genome['node_genes'])
    node1 = random.choice(genome['node_genes'])
    # TODO figure out recurrent and self connections

    new_connection_gene = connection_gene(node0['id'], node1['id'], innovation_number, weight=weight)
    genome['connection_genes'].append(new_connection_gene)


def add_node(genome):
    connection_id = random.randint(0, len(genome['connection_genes'])-1)
    genome['connection_genes'][connection_id]['expressed'] = False

    new_node = node_gene('hidden', next_node_id(genome))
    connection0 = connection_gene(genome['connection_genes'][connection_id]['input'])



def remove_connection(genome):
    connection_gene_id = random.randint(0, len(genome['connection_genes']-1))
    del genome['connection_genes'][connection_gene_id]
