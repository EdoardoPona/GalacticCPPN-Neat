
class NodeGene:

    def __init__(self, type, id):
        assert (type in ['input', 'output', 'hidden'])
        self.type = type
        self.id = id
        # self.innovation_number = innovation_number


class ConnectionGene:

    # TODO should we use node ids or can we use pointers to the actual nodes directly?
    def __init__(self, input_node_id, output_node_id, innovation_number, weight=1, expressed=True):
        self.input_node_id = input_node_id
        self.output_node_id = output_node_id
        self.innovation_number = innovation_number
        self.weight = weight
        self.expressed = expressed


class Genome:

    def __init__(self, node_genes=[], connection_genes=[]):
        self.node_genes = node_genes
        self.connection_genes = connection_genes
        self.fitness = 0

