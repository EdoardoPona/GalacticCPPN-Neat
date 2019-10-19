from models import *
import random


genome = Genome()


def next_node_id(genome):       # TODO this can be optimised by following suggestion 1 (see top)
    """ returns the next node id to be used (one larger than the current largest) """
    return max(list(genome.node_genes.keys())) + 1


def add_connection(genome, innovation_number, weight=1):
    """ adds a random connection between the two nodes """
    node0 = random.choice(genome.connection_genes)
    node1 = random.choice(genome.connection_genes)

    # TODO figure out recurrent and self connections
    new_connection_gene = ConnectionGene(node0.id, node1.id, innovation_number, weight)
    genome.connection_genes[innovation_number] = new_connection_gene


def add_node(genome, innovation_number):
    """ splits an existing connection in two and places a new node in the middle. Then creates two new connections in place
     of the old one, and disables the old connection """
    # innovation_number should be incremented by 2 after calling this function

    connection_id = random.randint(0, len(genome['connection_genes'])-1)
    genome.connection_genes[connection_id].expressed = False

    new_node = NodeGene('hidden', next_node_id(genome))

    connection0_weight = 1
    connection0 = ConnectionGene(genome.connection_genes[connection_id].input_node_id, new_node.id, innovation_number,
                                 weight=connection0_weight)
    genome.connection_genes[innovation_number] = connection0

    connection1_weight = genome.connection_genes[connection_id].weight          # out connection has the same weight at old connection
    connection1 = ConnectionGene(new_node.id, genome.connection_genes[connection_id].output_node_id, innovation_number+1,
                                 weight=connection1_weight)
    genome.connection_genes[innovation_number] = connection1
    genome.node_genes[new_node.id] = new_node


def remove_connection(genome):
    cg_innovation_number = random.randint(0, len(genome.connection_genes)-1)
    del genome.connection_genes[cg_innovation_number]


def crossover(fittest_genome, genome1):
    """ we are assuming fittest_genome to be fitter than genome1 """

    new_connection_genes = {}
    for inn_num in fittest_genome.get_innovation_numbers():
        if inn_num in genome1.get_innovation_numbers():
            new_connection_genes[inn_num] = random.choice([fittest_genome.connection_genes[inn_num], genome1.connection_genes[inn_num]])
        else:   # excess or disjoint gene, inheriting from the fittest gene
            new_connection_genes[inn_num] = fittest_genome.connection_genes[inn_num]

    # nodes are inherited from the fittest genome
    new_node_genes = {}
    for node in list(fittest_genome.items()):
        new_node_genes[node.id] = node


# TODO      excess_genes(), disjoint_genes() and average_weight_differences() will usually get called one after the other
# TODO      they all loop through all of the genes so they could probably be grouped into one function doing everything at the same time

def excess_genes(genome0, genome1):
    """ returns a list of the excess genes between genome0 and genome1 """
    excess_genes = []

    if max(genome0.get_innovation_numbers()) == max(genome1.get_innovation_numbers()):  # there are no excess genes
        return excess_genes

    genomes = [genome0, genome1]
    inn_nums = [max(genome0.get_innovation_numbers()), max(genome1.get_innovation_numbers())]
    max_id = inn_nums.index(max(inn_nums))          # genomes[max_id] is the longest genome
    min_inn_num = min(inn_nums)             # smallest of the two last innovation numbers. Excess genes start from here

    for inn_num in range(min_inn_num, max(inn_nums)):
        if inn_num in genomes[max_id].get_innovation_numbers():
            excess_genes.append(genomes[max_id].connection_genes[inn_num])

    return excess_genes


def disjoint_genes(genome0, genome1):
    """ returns a list of the disjoint genes between genome0 and genome1
    these are the genes which innovation numbers appear in only one of the genomes, but before the last innovation number
    of the shortest genome (they are not in the excessive part of the longer genome) """
    disjoint_genes = []
    for inn_num in range(min(genome0.get_innovation_numbers() + genome1.get_innovation_numbers())):
        if inn_num in genome0.get_innovation_numbers() and inn_num not in genome1.get_innovation_numbers():
            disjoint_genes.append(genome0.connection_genes[inn_num])
        elif inn_num not in genome0.get_innovation_numbers() and inn_num in genome1.get_innovation_numbers():
            disjoint_genes.append(genome1.connection_genes[inn_num])

    return disjoint_genes


def weight_differences(genome0, genome1):
    """ returns the connection weight differences between common connections in the two genomes """
    w_differences = []
    min_inn_num = min(max(genome0.get_innovation_numbers()), max(genome1.get_innovation_numbers()))
    for i in range(min_inn_num):
        if i in genome0.get_innovation_numbers() and i in genome1.get_innovation_numbers():
            w_differences.append(abs(genome0.connection_genes[i] - genome1.connection_genes[i]))
    return  w_differences


def compatibility_distance(genome0, genome1):
    N = max([len(genome0), len(genome1)])       # this is sometimes left as 1 if the lengths are smaller than 20 for example
    c0, c1, c2 = 1, 1, 1        # coefficients  # TODO what values should these have?
    E = len(excess_genes(genome0, genome1))
    D = len(disjoint_genes(genome0, genome1))
    w_differences = weight_differences(genome0, genome1)
    W = sum(w_differences) / len(w_differences)
    delta = c0*E/N + c1*D/N + c2*W


# TODO
def adjusted_fitness()

