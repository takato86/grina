import networkx as nx


def wrapper4parallel(args):
    fn, inner_args = args
    return fn(*inner_args)


def expansion_elongation(G, vertex):
    shortest_path_lengths = [
        path_length
        for path_length in nx.shortest_path_length(G, vertex).values()
    ]
    expansion = len(shortest_path_lengths) - 1
    elongation = max(shortest_path_lengths)
    return (vertex, expansion, elongation)