
# Basic implementation of de Bruijn graph assembler for short sequences

import argparse


class Node:
    def __init__(self, sequence):
        self.sequence = sequence
        self.next = {}

class Edge:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.count = 1
        self.source_sequences = set()

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input', help='input file with one sequence per line')
parser.add_argument('--k', help='kmer size, defaults to 30', type=int, default=30)
args = parser.parse_args()

# read in sequences from input file
sequences = []
with open(args.input, 'r') as file:
    for line in file:
        sequences.append(line.strip())

# store graph as a dictionary mapping {kmer sequence: Node}
graph = {}
# entry points into the graph (nodes with no incoming edges)
heads = []

for index, sequence in enumerate(sequences):
    # break each sequence into kmers
    kmers = [sequence[i : i + args.k] for i in range(len(sequence) - args.k + 1)]
    print(index, kmers)
    
    # put all kmers into the graph
    for i in range(len(kmers) - 1):

        kmer = kmers[i]
        next_kmer = kmers[i + 1]

        # make a Node for the kmer if there isn't one already
        # this will only happen for the first kmer of each sequence
        if kmer not in graph:
            graph[kmer] = Node(kmer)

            if graph[kmer] not in heads:
                heads.append(graph[kmer])

        # make a Node for the next kmer if there isn't one already
        if next_kmer not in graph:
            graph[next_kmer] = Node(next_kmer)

        # if the next kmer is listed as an entrypoint, remove it
        # because it no longer has 0 incoming edges
        if graph[next_kmer] in heads:
            heads.remove(graph[next_kmer])

        # store adjacency as edges
        if graph[next_kmer] in graph[kmer].next:
            edge = graph[kmer].next[graph[next_kmer]]
            edge.count += 1
        else:
            edge = Edge(graph[kmer], graph[next_kmer])
            graph[kmer].next[graph[next_kmer]] = edge

        # keep track of the sequences that this edge was observed in
        edge.source_sequences.add(index)


# def reverse_complement(sequence):
#     """Return the reverse complement of the sequence"""
#     base_pair = {
#         'A': 'T',
#         'T': 'A',
#         'G': 'C',
#         'C': 'G'
#     }
#     return ''.join([base_pair[base] for base in reversed(sequence)])


def print_paths(edges):
    """Recursively extend paths, print path when end is reached"""
    next_edges = list(edges[-1].end_node.next.values())

    if not next_edges or (len(next_edges) == 1 and next_edges[0].end_node is next_edges[0].start_node):
        print_sequence_from_kmers(edges)
        return

    for edge in next_edges:
        if edge.end_node is not node:
            print_paths(edges + [edge])


def print_sequence_from_kmers(edges):
    """Display the kmers as a graph and merged sequence"""
    graph_path = edges[0].start_node.sequence
    sequence = ''
    source_sequences = set()

    for edge in edges:

        graph_path += '--{}-->{}'.format(edge.count, edge.end_node.sequence)
        sequence += edge.start_node.sequence[0]
        source_sequences = source_sequences.union(edge.source_sequences)
    sequence += edge.end_node.sequence

    print(graph_path)
    print('Merged sequence:', sequence)
    print('Derived from sequences:', source_sequences)


# reformat node sequence to show possible repeats, if needed
for node in graph.values():
    if node in node.next:
        node.sequence = '({} * n)'.format(node.sequence)

# display all alignments originating from all entrypoints to the graph
for head in heads:
    for edge in head.next.values():
        print_paths([edge])

print('Number of alignments found:', len(heads))

