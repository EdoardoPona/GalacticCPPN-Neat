from models import *
import random


genome = Genome()


def next_node_id(genome):       # TODO this can be optimised by following suggestion 1 (see top)
    """ returns the next node id to be used (one larger than the current largest) """
    return max([node.id for node in genome.node_genes]) + 1


def add_connection(genome, innovation_number, weight=1):
    """ adds a random connection between the two nodes """
    node0 = random.choice(genome.connection_genes)
    node1 = random.choice(genome.connection_genes)

    # TODO figure out recurrent and self connections
    new_connection_gene = ConnectionGene(node0.id, node1.id, innovation_number, weight)
    genome.connection_genes.append(new_connection_gene)


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
    genome.connection_genes.append(connection0)

    connection1_weight = 1
    connection1 = ConnectionGene(new_node.id, genome.connection_genes[connection_id].output_node_id, innovation_number+1,
                                 weight=connection1_weight)
    genome.connection_genes.append(connection1)


def remove_connection(genome):
    connection_gene_id = random.randint(0, len(genome.connection_genes)-1)
    genome.connection_genes[connection_gene_id] = None      # this makes sure that all connection_gene lists are as long as the latest innovation number


def crossover(genome0, genome1):
    """ only genes that share the same innovation number can be mixed """
    # TODO this mehtod will be very inefficent, find a better one. Could be done by somehow indexing te connection genes
    # TODO by their innovation numbers since each genome must have hadd all the innovation numbers up to its largest one
    # TODO some could be missing though as they might have been removed
    new_connection_genes = []

    fittest_genome = None if genome0.fitness == genome1.fitness else genome0 if genome0.fitness > genome1.fitness else genome1

    max_innovation_number = max(len(genome0.connection_genes), len(genome1.connection_genes))
    for inn_num in range(max_innovation_number):
        if genome0.connection_genes[inn_num] is None or genome1.connection_genes[inn_num] is None:   # they are either disjoint or excess
            # inherit from the fittest parent
            if fittest_genome is None:      # the parent fitness is the same so we inherit randomly
                new_connection_genes.append(random.choice([genome0.connection_genes[inn_num], genome1.connection_genes[inn_num]]))
            else:
                new_connection_genes.append(fittest_genome.connection_genes[inn_num])
        else:       # both parents contain a gene with this innovation number so pick randomly
            # TODO figure out if genes with the same innovation number only differ by their connection weights (probably yes)
            new_connection_genes.append(random.choice([genome0.connection_genes[inn_num], genome1.connection_genes[inn_num]]))

